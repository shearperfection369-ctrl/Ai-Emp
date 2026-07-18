"""Iteration 2 backend tests: bundles, tiers, reviews, bundle checkout, library expansion."""
import os
import uuid
import time
import asyncio
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://ready-to-use-ai.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

ADMIN_EMAIL = "admin@aitoolemporium.com"
ADMIN_PASSWORD = "Emporium@2026"


@pytest.fixture(scope="module")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def user_session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    email = f"TEST_it2_{uuid.uuid4().hex[:8]}@example.com"
    r = s.post(f"{API}/auth/register",
               json={"name": "It2 User", "email": email, "password": "password123"}, timeout=15)
    assert r.status_code == 200, f"register failed: {r.text}"
    s._email = email
    s._user_id = r.json()["user"]["user_id"]
    return s


# ---------- Bundles ----------
class TestBundles:
    def test_list_bundles(self, http):
        r = http.get(f"{API}/bundles", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list) and len(data) == 4
        slugs = {b["slug"] for b in data}
        assert {"creator-pack", "growth-engine", "founders-toolkit", "career-launch"} == slugs
        for b in data:
            assert b["lookup_key"] == f"bundle_{b['slug']}"
            assert b["price"] > 0
            assert b["original_price"] >= b["price"]
            assert b["savings_pct"] >= 0
            assert isinstance(b["tools"], list) and len(b["tools"]) >= 2
            for t in b["tools"]:
                assert set(["slug", "name", "icon", "price"]).issubset(t.keys())

    def test_creator_pack_savings(self, http):
        r = http.get(f"{API}/bundles", timeout=10)
        data = r.json()
        cp = next(b for b in data if b["slug"] == "creator-pack")
        assert cp["price"] == 99
        assert cp["savings_pct"] > 20
        assert {t["slug"] for t in cp["tools"]} == {"storyforge", "socialpulse", "emailgenie"}

    def test_bundle_detail(self, http):
        r = http.get(f"{API}/bundles/creator-pack", timeout=10)
        assert r.status_code == 200
        b = r.json()
        assert b["slug"] == "creator-pack"
        assert b["lookup_key"] == "bundle_creator-pack"
        assert len(b["tools"]) == 3
        for t in b["tools"]:
            assert "tagline" in t

    def test_bundle_unknown_slug_404(self, http):
        r = http.get(f"{API}/bundles/does-not-exist", timeout=10)
        assert r.status_code == 404


# ---------- Tier / speed / why enrichment ----------
class TestTiers:
    def test_tools_list_has_tier(self, http):
        r = http.get(f"{API}/tools", timeout=10)
        assert r.status_code == 200
        data = r.json()
        # Iteration 3: catalog expanded to 65 tools; keep this test forward-compatible
        assert len(data) >= 18
        for t in data:
            assert t.get("tier") in ("Bronze", "Silver", "Gold"), f"missing tier on {t['slug']}"
            assert t.get("speed") in ("Instant", "Fast", "Deep")
            assert t.get("quality_tier"), f"missing quality_tier on {t['slug']}"
            assert isinstance(t.get("why"), str) and len(t["why"]) > 5

    def test_tool_detail_has_tier(self, http):
        r = http.get(f"{API}/tools/neurocopy", timeout=10)
        assert r.status_code == 200
        t = r.json()
        assert t["tier"] == "Gold"
        assert t["speed"] == "Fast"
        assert t["quality_tier"]
        assert "why" in t and t["why"]


# ---------- Reviews ----------
class TestReviews:
    def test_reviews_seeded_for_neurocopy(self, http):
        r = http.get(f"{API}/tools/neurocopy/reviews", timeout=10)
        assert r.status_code == 200
        d = r.json()
        assert d["count"] >= 2
        assert d["average"] >= 4.5
        assert isinstance(d["reviews"], list) and len(d["reviews"]) == d["count"]
        for rev in d["reviews"]:
            assert "user_name" in rev and "rating" in rev and "comment" in rev

    def test_reviews_unknown_tool_returns_empty(self, http):
        r = http.get(f"{API}/tools/does-not-exist-xyz/reviews", timeout=10)
        # GET returns empty rather than 404 by design; accept either
        assert r.status_code in (200, 404)
        if r.status_code == 200:
            d = r.json()
            assert d["count"] == 0
            assert d["reviews"] == []

    def test_post_review_requires_auth(self, http):
        r = http.post(f"{API}/tools/neurocopy/reviews", json={"rating": 5, "comment": "great"}, timeout=10)
        assert r.status_code == 401

    def test_post_review_bad_rating_422(self, user_session):
        r = user_session.post(f"{API}/tools/neurocopy/reviews", json={"rating": 9, "comment": "x"}, timeout=10)
        assert r.status_code == 422

    def test_post_review_unknown_tool_404(self, user_session):
        r = user_session.post(f"{API}/tools/does-not-exist-xyz/reviews",
                              json={"rating": 5, "comment": "hey"}, timeout=10)
        assert r.status_code == 404

    def test_post_review_creates_unverified(self, user_session):
        r = user_session.post(f"{API}/tools/storyforge/reviews",
                              json={"rating": 4, "comment": "TEST first review comment"}, timeout=10)
        assert r.status_code == 200
        d = r.json()
        assert d["rating"] == 4
        assert d["verified"] is False  # user has no paid txn yet
        # Confirm via GET
        got = user_session.get(f"{API}/tools/storyforge/reviews", timeout=10).json()
        assert any(rv["comment"] == "TEST first review comment" and rv["user_id"] == user_session._user_id
                   for rv in got["reviews"])

    def test_post_review_upsert(self, user_session):
        # Post twice with same user; count/existing entry should not double.
        before = user_session.get(f"{API}/tools/storyforge/reviews", timeout=10).json()
        mine_before = [r for r in before["reviews"] if r["user_id"] == user_session._user_id]
        user_session.post(f"{API}/tools/storyforge/reviews",
                          json={"rating": 5, "comment": "TEST updated comment"}, timeout=10)
        after = user_session.get(f"{API}/tools/storyforge/reviews", timeout=10).json()
        mine_after = [r for r in after["reviews"] if r["user_id"] == user_session._user_id]
        assert len(mine_after) == 1, "review should upsert, not duplicate"
        assert mine_after[0]["rating"] == 5
        assert mine_after[0]["comment"] == "TEST updated comment"
        # Overall user's contribution count unchanged
        assert len(mine_after) == len(mine_before) if mine_before else True


# ---------- Bundle checkout regression ----------
class TestBundleCheckout:
    def test_checkout_bundle_creates_session(self, user_session):
        r = user_session.post(
            f"{API}/payments/checkout",
            json={"items": [{"lookup_key": "bundle_creator-pack", "quantity": 1}],
                  "origin_url": BASE_URL},
            timeout=30,
        )
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["checkout_url"].startswith("https://")
        assert d["session_id"].startswith("cs_")
        TestBundleCheckout._sid = d["session_id"]

    def test_bundle_transaction_stored(self, http):
        # Give backend a moment to persist
        time.sleep(1)
        sid = getattr(TestBundleCheckout, "_sid", None)
        assert sid
        # Use payments/status which returns the persisted items array
        r = http.get(f"{API}/payments/status/{sid}", timeout=15)
        assert r.status_code == 200
        d = r.json()
        assert len(d["items"]) == 1
        item = d["items"][0]
        assert item.get("is_bundle") is True
        assert set(item.get("included_slugs", [])) == {"storyforge", "socialpulse", "emailgenie"}


# ---------- Library bundle expansion (direct DB simulation) ----------
class TestLibraryBundleExpansion:
    def test_library_expands_bundle(self):
        """Simulate a paid bundle purchase by inserting a payment_transactions doc, then verify /library."""
        import os as _os
        from motor.motor_asyncio import AsyncIOMotorClient
        from datetime import datetime, timezone

        async def run():
            client = AsyncIOMotorClient(_os.environ["MONGO_URL"])
            db = client[_os.environ["DB_NAME"]]
            # Fresh test user
            s = requests.Session()
            s.headers.update({"Content-Type": "application/json"})
            email = f"TEST_libexp_{uuid.uuid4().hex[:8]}@example.com"
            reg = s.post(f"{API}/auth/register",
                         json={"name": "LibExp", "email": email, "password": "password123"}, timeout=15)
            assert reg.status_code == 200
            uid = reg.json()["user"]["user_id"]
            # Insert paid bundle transaction
            await db.payment_transactions.insert_one({
                "session_id": f"cs_test_TEST_{uuid.uuid4().hex[:12]}",
                "user_id": uid,
                "user_email": email,
                "items": [{
                    "slug": "creator-pack", "name": "Creator Pack",
                    "lookup_key": "bundle_creator-pack",
                    "price": 99.0, "quantity": 1,
                    "is_bundle": True,
                    "included_slugs": ["storyforge", "socialpulse", "emailgenie"],
                }],
                "amount": 99.0,
                "currency": "usd",
                "status": "completed",
                "payment_status": "paid",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            })
            lib = s.get(f"{API}/library", timeout=10)
            assert lib.status_code == 200
            data = lib.json()
            slugs = {t["slug"] for t in data}
            assert {"storyforge", "socialpulse", "emailgenie"}.issubset(slugs), \
                f"library did not expand bundle. got: {slugs}"
            # cleanup
            await db.payment_transactions.delete_many({"user_id": uid})
            await db.users.delete_one({"user_id": uid})
            await db.user_sessions.delete_many({"user_id": uid})
            client.close()

        asyncio.get_event_loop().run_until_complete(run()) if False else asyncio.run(run())


# ---------- Verified-review flow (post-bundle purchase) ----------
class TestVerifiedReview:
    def test_verified_after_paid_bundle(self):
        """Insert a paid bundle txn, then POST a review => verified=True."""
        import os as _os
        from motor.motor_asyncio import AsyncIOMotorClient
        from datetime import datetime, timezone

        async def run():
            client = AsyncIOMotorClient(_os.environ["MONGO_URL"])
            db = client[_os.environ["DB_NAME"]]
            s = requests.Session()
            s.headers.update({"Content-Type": "application/json"})
            email = f"TEST_vfy_{uuid.uuid4().hex[:8]}@example.com"
            reg = s.post(f"{API}/auth/register",
                         json={"name": "Vfy", "email": email, "password": "password123"}, timeout=15)
            uid = reg.json()["user"]["user_id"]
            await db.payment_transactions.insert_one({
                "session_id": f"cs_test_TEST_{uuid.uuid4().hex[:12]}",
                "user_id": uid, "user_email": email,
                "items": [{
                    "slug": "creator-pack", "name": "Creator Pack",
                    "lookup_key": "bundle_creator-pack",
                    "price": 99.0, "quantity": 1,
                    "is_bundle": True,
                    "included_slugs": ["storyforge", "socialpulse", "emailgenie"],
                }],
                "amount": 99.0, "currency": "usd",
                "status": "completed", "payment_status": "paid",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            })
            r = s.post(f"{API}/tools/storyforge/reviews",
                       json={"rating": 5, "comment": "TEST verified after bundle"}, timeout=10)
            assert r.status_code == 200
            assert r.json()["verified"] is True
            # cleanup
            await db.payment_transactions.delete_many({"user_id": uid})
            await db.reviews.delete_many({"user_id": uid})
            await db.users.delete_one({"user_id": uid})
            await db.user_sessions.delete_many({"user_id": uid})
            client.close()

        asyncio.run(run())
