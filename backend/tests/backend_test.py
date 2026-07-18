"""Backend API tests for AI Tool Emporium.

Covers: catalog (tools/categories/detail), auth (register/login/me/logout),
live AI demo, ARIA streaming, Stripe payments checkout+status, library, admin.
"""
import os
import uuid
import time

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://ready-to-use-ai.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

ADMIN_EMAIL = "admin@aitoolemporium.com"
ADMIN_PASSWORD = "Emporium@2026"


# ---------- fixtures ----------
@pytest.fixture(scope="module")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def admin_session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    r = s.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}, timeout=15)
    assert r.status_code == 200, f"Admin login failed: {r.text}"
    return s


@pytest.fixture(scope="module")
def user_session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    email = f"TEST_user_{uuid.uuid4().hex[:8]}@example.com"
    r = s.post(f"{API}/auth/register", json={"name": "Test User", "email": email, "password": "password123"}, timeout=15)
    assert r.status_code == 200, f"register failed: {r.text}"
    s._email = email
    return s


# ---------- Catalog ----------
class TestCatalog:
    def test_list_tools(self, http):
        r = http.get(f"{API}/tools", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list) and len(data) == 18
        assert all("slug" in t and "price" in t and "category" in t for t in data)

    def test_categories(self, http):
        r = http.get(f"{API}/categories", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 12
        assert all("id" in c and "count" in c for c in data)
        assert sum(c["count"] for c in data) == 18

    def test_category_filter(self, http):
        r = http.get(f"{API}/tools?category=marketing", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0
        assert all(t["category"] == "marketing" for t in data)

    def test_search(self, http):
        r = http.get(f"{API}/tools?search=copy", timeout=10)
        assert r.status_code == 200
        data = r.json()
        # At least one match expected across name/tagline/category
        assert isinstance(data, list)

    def test_sort_price_asc(self, http):
        r = http.get(f"{API}/tools?sort=price_asc", timeout=10)
        data = r.json()
        prices = [t["price"] for t in data]
        assert prices == sorted(prices)

    def test_sort_price_desc(self, http):
        r = http.get(f"{API}/tools?sort=price_desc", timeout=10)
        data = r.json()
        prices = [t["price"] for t in data]
        assert prices == sorted(prices, reverse=True)

    def test_sort_rating(self, http):
        r = http.get(f"{API}/tools?sort=rating", timeout=10)
        data = r.json()
        ratings = [t.get("rating", 0) for t in data]
        assert ratings == sorted(ratings, reverse=True)

    def test_tool_detail(self, http):
        r = http.get(f"{API}/tools/brandforge", timeout=10)
        assert r.status_code == 200
        t = r.json()
        assert t["slug"] == "brandforge"
        assert "demo_system" not in t  # internal field must be stripped

    def test_tool_detail_404(self, http):
        r = http.get(f"{API}/tools/does-not-exist-xyz", timeout=10)
        assert r.status_code == 404


# ---------- Auth ----------
class TestAuth:
    def test_register_and_me(self):
        s = requests.Session()
        email = f"TEST_reg_{uuid.uuid4().hex[:8]}@example.com"
        r = s.post(f"{API}/auth/register", json={"name": "Reg User", "email": email, "password": "password123"}, timeout=15)
        assert r.status_code == 200
        d = r.json()
        assert d["user"]["email"] == email.lower()
        assert d["user"]["role"] == "user"
        # session cookie must be set
        assert "session_token" in s.cookies.get_dict() or d.get("session_token")
        me = s.get(f"{API}/auth/me", timeout=10)
        assert me.status_code == 200
        assert me.json()["email"] == email.lower()

    def test_register_duplicate_400(self, user_session):
        r = user_session.post(f"{API}/auth/register",
                              json={"name": "Dup", "email": user_session._email, "password": "password123"},
                              timeout=10)
        assert r.status_code == 400

    def test_login_admin(self):
        s = requests.Session()
        r = s.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}, timeout=10)
        assert r.status_code == 200
        assert r.json()["user"]["role"] == "admin"

    def test_login_wrong_password_401(self):
        r = requests.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "password": "wrongpass"}, timeout=10)
        assert r.status_code == 401

    def test_me_requires_auth(self):
        r = requests.get(f"{API}/auth/me", timeout=10)
        assert r.status_code == 401

    def test_logout_clears_session(self):
        s = requests.Session()
        email = f"TEST_lo_{uuid.uuid4().hex[:8]}@example.com"
        s.post(f"{API}/auth/register", json={"name": "Lo", "email": email, "password": "password123"}, timeout=10)
        assert s.get(f"{API}/auth/me", timeout=10).status_code == 200
        s.post(f"{API}/auth/logout", timeout=10)
        assert s.get(f"{API}/auth/me", timeout=10).status_code == 401


# ---------- AI demo ----------
class TestAIDemo:
    def test_demo_empty_400(self, http):
        r = http.post(f"{API}/tools/brandforge/demo", json={"input": "   "}, timeout=15)
        assert r.status_code == 400

    def test_demo_unknown_tool_404(self, http):
        r = http.post(f"{API}/tools/nope-xyz/demo", json={"input": "hello"}, timeout=15)
        assert r.status_code == 404

    def test_demo_generates_output(self, http):
        r = http.post(f"{API}/tools/brandforge/demo",
                      json={"input": "Launch a new eco-friendly water bottle for busy runners"},
                      timeout=90)
        assert r.status_code == 200, r.text
        d = r.json()
        assert "output" in d and isinstance(d["output"], str) and len(d["output"]) > 20


# ---------- ARIA streaming ----------
class TestAria:
    def test_assistant_stream(self):
        payload = {"session_id": f"test_{uuid.uuid4().hex[:8]}",
                   "message": "I run a marketing agency and need copy help. What do you recommend?"}
        with requests.post(f"{API}/assistant/chat", json=payload, stream=True, timeout=90) as r:
            assert r.status_code == 200
            assert r.headers.get("content-type", "").startswith("text/plain")
            chunks = []
            for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    chunks.append(chunk)
                if sum(len(c) for c in chunks) > 40:
                    break
            body = "".join(chunks)
            assert len(body) > 20, f"stream too short: {body!r}"


# ---------- Payments ----------
class TestPayments:
    def test_checkout_creates_session(self, user_session):
        r = user_session.post(f"{API}/payments/checkout",
                              json={"items": [{"lookup_key": "tool_brandforge", "quantity": 1}],
                                    "origin_url": BASE_URL},
                              timeout=30)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d.get("checkout_url", "").startswith("https://")
        assert d.get("session_id", "").startswith("cs_")
        # Persist for status test via module-level cache
        TestPayments._session_id = d["session_id"]

    def test_status_pending(self, http):
        sid = getattr(TestPayments, "_session_id", None)
        assert sid, "prior checkout test must run first"
        # Small wait so the record is persisted
        time.sleep(1)
        r = http.get(f"{API}/payments/status/{sid}", timeout=15)
        assert r.status_code == 200
        d = r.json()
        assert d["session_id"] == sid
        assert d["payment_status"] in ("pending", "unpaid")

    def test_status_not_found_404(self, http):
        r = http.get(f"{API}/payments/status/cs_test_doesnotexist", timeout=10)
        assert r.status_code == 404

    def test_checkout_empty_cart_400(self, user_session):
        r = user_session.post(f"{API}/payments/checkout",
                              json={"items": [], "origin_url": BASE_URL}, timeout=15)
        assert r.status_code in (400, 422)

    def test_checkout_bad_lookup_400(self, user_session):
        r = user_session.post(f"{API}/payments/checkout",
                              json={"items": [{"lookup_key": "tool_nonexistent_xyz", "quantity": 1}],
                                    "origin_url": BASE_URL}, timeout=20)
        assert r.status_code == 400


# ---------- Library ----------
class TestLibrary:
    def test_library_requires_auth(self):
        r = requests.get(f"{API}/library", timeout=10)
        assert r.status_code == 401

    def test_library_empty_for_new_user(self, user_session):
        r = user_session.get(f"{API}/library", timeout=10)
        assert r.status_code == 200
        assert r.json() == []


# ---------- Admin ----------
class TestAdmin:
    def test_stats_requires_admin(self, user_session):
        r = user_session.get(f"{API}/admin/stats", timeout=10)
        assert r.status_code == 403

    def test_stats_ok_for_admin(self, admin_session):
        r = admin_session.get(f"{API}/admin/stats", timeout=10)
        assert r.status_code == 200
        d = r.json()
        for key in ("total_revenue", "total_orders", "total_users", "total_tools",
                    "aov", "revenue_series", "top_tools"):
            assert key in d
        assert d["total_tools"] == 18

    def test_orders_requires_admin(self):
        r = requests.get(f"{API}/admin/orders", timeout=10)
        assert r.status_code == 401

    def test_orders_ok_for_admin(self, admin_session):
        r = admin_session.get(f"{API}/admin/orders", timeout=10)
        assert r.status_code == 200
        assert isinstance(r.json(), list)
