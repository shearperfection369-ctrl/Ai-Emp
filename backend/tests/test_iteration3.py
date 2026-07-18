"""Iteration 3 backend tests: expanded catalog (65 tools / 31 categories), everyday tier,
new-tool tier/why enrichment, Stripe prices for new products, and new-tool AI demo."""
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


@pytest.fixture(scope="module")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# ---------- Expanded catalog totals ----------
class TestCatalogExpansion:
    def test_65_tools(self, http):
        r = http.get(f"{API}/tools", timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 65, f"expected 65 tools, got {len(data)}"

    def test_31_categories_no_empty(self, http):
        r = http.get(f"{API}/categories", timeout=15)
        assert r.status_code == 200
        cats = r.json()
        assert len(cats) == 31, f"expected 31 categories, got {len(cats)}"
        empty = [c["id"] for c in cats if c.get("count", 0) <= 0]
        assert not empty, f"empty categories found (count<=0): {empty}"
        # Total per-category sums back to 65 tools
        assert sum(c["count"] for c in cats) == 65

    def test_all_tools_have_tier_speed_quality_why(self, http):
        """Every tool from /api/tools must have tier/speed/quality_tier/why populated
        (including newly added tools like freightpilot/mealmate/giftgenie/threatlens)."""
        tools = http.get(f"{API}/tools", timeout=15).json()
        missing = []
        for t in tools:
            if t.get("tier") not in ("Bronze", "Silver", "Gold"):
                missing.append((t["slug"], "tier"))
            if t.get("speed") not in ("Instant", "Fast", "Deep"):
                missing.append((t["slug"], "speed"))
            if not t.get("quality_tier"):
                missing.append((t["slug"], "quality_tier"))
            if not (isinstance(t.get("why"), str) and len(t["why"].strip()) > 10):
                missing.append((t["slug"], "why"))
        assert not missing, f"tools missing enrichment fields: {missing[:10]}"

        # Explicit spot-check on called-out tools
        by_slug = {t["slug"]: t for t in tools}
        for slug in ("freightpilot", "mealmate", "giftgenie", "threatlens"):
            assert slug in by_slug, f"missing new tool {slug}"
            t = by_slug[slug]
            assert t["tier"] in ("Bronze", "Silver", "Gold")
            assert t["speed"] in ("Instant", "Fast", "Deep")
            assert t["quality_tier"]
            assert t["why"] and len(t["why"]) > 10


# ---------- Everyday Life category ----------
class TestEverydayCategory:
    EXPECTED = {"mealmate", "budgetbuddy", "studybuddy", "giftgenie",
                "chefai", "lingualoop", "planmyday", "wordsmith"}

    def test_everyday_returns_8_tools(self, http):
        r = http.get(f"{API}/tools?category=everyday", timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 8, f"expected 8 everyday tools, got {len(data)}"
        assert {t["slug"] for t in data} == self.EXPECTED
        # Every everyday tool must be $9-$29 (affordable band)
        for t in data:
            assert 9 <= t["price"] <= 29, f"{t['slug']} price {t['price']} outside $9-$29"
            assert t["category"] == "everyday"


# ---------- New industry category filters ----------
class TestNewCategoryFilters:
    @pytest.mark.parametrize("cat", ["logistics", "healthcare", "cybersecurity", "everyday"])
    def test_category_filter_returns_only_that_category(self, http, cat):
        r = http.get(f"{API}/tools?category={cat}", timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0, f"no tools returned for {cat}"
        for t in data:
            assert t["category"] == cat, f"{t['slug']} not in category {cat}"


# ---------- Stripe checkout: new products (price sync check) ----------
class TestStripeCheckoutNewTools:
    ORIGIN = BASE_URL

    def test_checkout_giftgenie(self, http):
        r = http.post(
            f"{API}/payments/checkout",
            json={"items": [{"lookup_key": "tool_giftgenie", "quantity": 1}],
                  "origin_url": self.ORIGIN},
            timeout=30,
        )
        assert r.status_code == 200, f"giftgenie checkout failed: {r.text}"
        d = r.json()
        assert d["checkout_url"].startswith("https://checkout.stripe.com"), \
            f"expected https://checkout.stripe.com, got {d['checkout_url']}"
        assert d["session_id"].startswith("cs_")

    def test_checkout_threatlens(self, http):
        r = http.post(
            f"{API}/payments/checkout",
            json={"items": [{"lookup_key": "tool_threatlens", "quantity": 1}],
                  "origin_url": self.ORIGIN},
            timeout=30,
        )
        assert r.status_code == 200, f"threatlens checkout failed: {r.text}"
        d = r.json()
        assert d["checkout_url"].startswith("https://checkout.stripe.com"), \
            f"expected https://checkout.stripe.com, got {d['checkout_url']}"
        assert d["session_id"].startswith("cs_")

    def test_checkout_freightpilot(self, http):
        r = http.post(
            f"{API}/payments/checkout",
            json={"items": [{"lookup_key": "tool_freightpilot", "quantity": 1}],
                  "origin_url": self.ORIGIN},
            timeout=30,
        )
        assert r.status_code == 200, f"freightpilot checkout failed: {r.text}"
        assert r.json()["checkout_url"].startswith("https://checkout.stripe.com")


# ---------- New-tool AI demo endpoint ----------
class TestNewToolDemo:
    def test_mealmate_demo_returns_output(self, http):
        r = http.post(
            f"{API}/tools/mealmate/demo",
            json={"input": "Healthy dinners for a family of 4, no seafood, $100 budget"},
            timeout=90,
        )
        assert r.status_code == 200, f"demo failed: {r.text}"
        d = r.json()
        assert d.get("tool") == "MealMate"
        assert isinstance(d.get("output"), str) and len(d["output"].strip()) > 50, \
            f"output too short: {d.get('output')!r}"


# ---------- Regression: bundles still 4 ----------
class TestBundleRegression:
    def test_bundles_still_four(self, http):
        r = http.get(f"{API}/bundles", timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 4
        assert {b["slug"] for b in data} == {"creator-pack", "growth-engine",
                                             "founders-toolkit", "career-launch"}
