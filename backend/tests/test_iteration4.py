"""Iteration 4 backend tests: AI Studio (credit-metered image/text/research),
credits enforcement (HTTP 402), credit packs (3), Stripe checkout for credit packs.
Uses a FRESH registered user for clean credit-math."""
import os
import uuid
import time
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL",
                          "https://ready-to-use-ai.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

FREE_CREDITS = 30
COST_TEXT = 2
COST_RESEARCH = 4
COST_IMAGE = 15


def _register_fresh_user():
    """Register a brand-new user; returns (session_with_auth, user_dict)."""
    email = f"TEST_studio_{uuid.uuid4().hex[:10]}@example.com"
    password = "Test@123456"
    name = "Studio Tester"
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    r = s.post(f"{API}/auth/register",
               json={"name": name, "email": email, "password": password}, timeout=15)
    assert r.status_code == 200, f"register failed: {r.status_code} {r.text}"
    data = r.json()
    # server sets httpOnly cookie AND returns token; also add bearer to be safe
    tok = data.get("access_token") or data.get("token")
    if tok:
        s.headers.update({"Authorization": f"Bearer {tok}"})
    return s, data.get("user", {}), email, password


@pytest.fixture(scope="module")
def fresh_user():
    s, u, email, pw = _register_fresh_user()
    return {"session": s, "user": u, "email": email, "password": pw}


# ---------- /api/studio/credits ----------
class TestStudioCredits:
    def test_credits_endpoint_requires_auth(self):
        r = requests.get(f"{API}/studio/credits", timeout=15)
        assert r.status_code in (401, 403), f"expected 401/403, got {r.status_code}"

    def test_credits_fresh_user_starts_with_30(self, fresh_user):
        r = fresh_user["session"].get(f"{API}/studio/credits", timeout=15)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["credits"] == FREE_CREDITS, f"expected {FREE_CREDITS}, got {data['credits']}"
        assert data["costs"] == {"text": COST_TEXT, "research": COST_RESEARCH, "image": COST_IMAGE}


# ---------- /api/credit-packs ----------
class TestCreditPacks:
    def test_three_packs_correct(self):
        r = requests.get(f"{API}/credit-packs", timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 3
        by_slug = {p["slug"]: p for p in data}
        assert set(by_slug) == {"spark", "pro", "studio"}

        assert by_slug["spark"]["credits"] == 120
        assert by_slug["spark"]["price"] == 9
        assert by_slug["spark"]["lookup_key"] == "credits_spark"

        assert by_slug["pro"]["credits"] == 350
        assert by_slug["pro"]["price"] == 19
        assert by_slug["pro"]["lookup_key"] == "credits_pro"

        assert by_slug["studio"]["credits"] == 800
        assert by_slug["studio"]["price"] == 29
        assert by_slug["studio"]["lookup_key"] == "credits_studio"


# ---------- Text generation (2 credits, chatgpt/claude) ----------
class TestStudioText:
    def test_empty_prompt_returns_400(self, fresh_user):
        r = fresh_user["session"].post(f"{API}/studio/text",
                                       json={"mode": "chatgpt", "prompt": "   "}, timeout=30)
        assert r.status_code == 400

    def test_text_chatgpt_deducts_2_and_mentions_gpt(self, fresh_user):
        s = fresh_user["session"]
        # get current balance
        bal_before = s.get(f"{API}/studio/credits", timeout=15).json()["credits"]
        r = s.post(f"{API}/studio/text",
                   json={"mode": "chatgpt", "prompt": "Write a one-line hello world tagline."},
                   timeout=90)
        assert r.status_code == 200, f"text chatgpt failed: {r.status_code} {r.text}"
        d = r.json()
        assert isinstance(d.get("output"), str) and len(d["output"].strip()) > 3
        assert "GPT" in d.get("engine", ""), f"engine should mention GPT: {d.get('engine')}"
        assert d["credits"] == bal_before - COST_TEXT
        # verify persisted
        bal_after = s.get(f"{API}/studio/credits", timeout=15).json()["credits"]
        assert bal_after == bal_before - COST_TEXT

    def test_text_claude_deducts_2_and_mentions_claude(self, fresh_user):
        s = fresh_user["session"]
        bal_before = s.get(f"{API}/studio/credits", timeout=15).json()["credits"]
        r = s.post(f"{API}/studio/text",
                   json={"mode": "claude", "prompt": "One-word: sky color?"},
                   timeout=90)
        assert r.status_code == 200, f"text claude failed: {r.status_code} {r.text}"
        d = r.json()
        assert "Claude" in d.get("engine", ""), f"engine should mention Claude: {d.get('engine')}"
        assert d["credits"] == bal_before - COST_TEXT


# ---------- Research (4 credits) ----------
class TestStudioResearch:
    def test_research_deducts_4(self, fresh_user):
        s = fresh_user["session"]
        bal_before = s.get(f"{API}/studio/credits", timeout=15).json()["credits"]
        r = s.post(f"{API}/studio/research",
                   json={"query": "Briefly: pros and cons of remote work."},
                   timeout=90)
        assert r.status_code == 200, f"research failed: {r.status_code} {r.text}"
        d = r.json()
        assert isinstance(d.get("output"), str) and len(d["output"].strip()) > 20
        assert d["credits"] == bal_before - COST_RESEARCH


# ---------- Image (15 credits, slow — up to 60s) ----------
class TestStudioImage:
    def test_image_deducts_15_and_returns_base64(self, fresh_user):
        s = fresh_user["session"]
        bal_before = s.get(f"{API}/studio/credits", timeout=15).json()["credits"]
        r = s.post(f"{API}/studio/image",
                   json={"prompt": "A simple neon blue circle on a dark background, minimalist."},
                   timeout=120)
        assert r.status_code == 200, f"image failed: {r.status_code} {r.text}"
        d = r.json()
        b64 = d.get("image_base64", "")
        assert isinstance(b64, str) and len(b64) > 1000, f"base64 too short: {len(b64)}"
        assert d["credits"] == bal_before - COST_IMAGE


# ---------- Credits enforcement (HTTP 402) ----------
class TestCreditsEnforcement:
    """Drain a fresh user's credits, then verify HTTP 402 with no deduction."""

    def test_402_when_insufficient_credits_and_no_deduction(self):
        # Fresh user with 30 credits. Do 1 image (-15 = 15). Then a text (-2 = 13).
        # Then try image (needs 15, has 13) -> 402.
        s, _u, _e, _p = _register_fresh_user()

        # spend image (15)
        r = s.post(f"{API}/studio/image",
                   json={"prompt": "A tiny red square, minimalist."}, timeout=120)
        assert r.status_code == 200, f"first image failed: {r.text}"
        assert r.json()["credits"] == 15

        # spend text (2) -> 13
        r = s.post(f"{API}/studio/text",
                   json={"mode": "claude", "prompt": "Say hi in 3 words."}, timeout=60)
        assert r.status_code == 200, f"text failed: {r.text}"
        assert r.json()["credits"] == 13

        # attempt another image (15) with only 13 -> 402
        r = s.post(f"{API}/studio/image",
                   json={"prompt": "Another tiny square."}, timeout=30)
        assert r.status_code == 402, f"expected 402, got {r.status_code}: {r.text}"

        # Balance must be unchanged after 402
        bal = s.get(f"{API}/studio/credits", timeout=15).json()["credits"]
        assert bal == 13, f"balance changed on 402: {bal}"


# ---------- Stripe checkout for credit packs ----------
class TestCreditPackCheckout:
    ORIGIN = BASE_URL

    def _checkout(self, lookup_key):
        r = requests.post(f"{API}/payments/checkout",
                          json={"items": [{"lookup_key": lookup_key, "quantity": 1}],
                                "origin_url": self.ORIGIN},
                          timeout=30)
        return r

    def test_checkout_credits_pro_returns_stripe_url(self):
        r = self._checkout("credits_pro")
        assert r.status_code == 200, f"credits_pro checkout failed: {r.text}"
        d = r.json()
        assert d["checkout_url"].startswith("https://checkout.stripe.com"), d["checkout_url"]
        assert d["session_id"].startswith("cs_")

    def test_checkout_credits_spark_returns_stripe_url(self):
        r = self._checkout("credits_spark")
        assert r.status_code == 200, f"credits_spark checkout failed: {r.text}"
        assert r.json()["checkout_url"].startswith("https://checkout.stripe.com")

    def test_checkout_credits_studio_returns_stripe_url(self):
        r = self._checkout("credits_studio")
        assert r.status_code == 200, f"credits_studio checkout failed: {r.text}"
        assert r.json()["checkout_url"].startswith("https://checkout.stripe.com")


# ---------- Regression: nav / marketplace still work ----------
class TestRegression:
    def test_tools_still_65(self):
        r = requests.get(f"{API}/tools", timeout=15)
        assert r.status_code == 200
        assert len(r.json()) == 65

    def test_bundles_still_4(self):
        r = requests.get(f"{API}/bundles", timeout=15)
        assert r.status_code == 200
        assert len(r.json()) == 4
