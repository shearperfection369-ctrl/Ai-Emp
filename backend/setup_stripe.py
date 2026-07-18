"""Idempotent Stripe catalog setup for AI Tool Emporium. Creates a Product + one-time Price per tool."""
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

import os
import stripe
from catalog import CATALOG, BUNDLES

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY") or "sk_test_emergent"

DIGITAL_TAX_CODE = "txcd_10000000"  # general digital goods


def ensure_tax_settings():
    s = stripe.tax.Settings.retrieve()
    if s.head_office and getattr(s.head_office, "address", None):
        return
    try:
        stripe.tax.Settings.modify(
            head_office={"address": {"country": "US", "line1": "1 Market St",
                                     "city": "San Francisco", "state": "CA", "postal_code": "94105"}},
            defaults={"tax_behavior": "exclusive"},
        )
    except Exception as e:
        print("tax settings note:", e)


def get_or_create_product(entry):
    for p in stripe.Product.list(active=True, limit=100).auto_paging_iter():
        if p.to_dict().get("metadata", {}).get("emergent_product_id") == entry["slug"]:
            return p
    return stripe.Product.create(
        name=entry["name"],
        description=entry["tagline"],
        tax_code=DIGITAL_TAX_CODE,
        metadata={"managed_by": "emergent", "emergent_product_id": entry["slug"]},
    )


def ensure_price(product, entry):
    lookup_key = entry["lookup_key"]
    amount = entry["amount_cents"]
    existing = stripe.Price.list(lookup_keys=[lookup_key], active=True, limit=1).data
    if existing and existing[0].unit_amount != amount:
        stripe.Price.modify(existing[0].id, active=False)
        existing = []
    if not existing:
        stripe.Price.create(
            product=product.id, unit_amount=amount, currency="usd",
            lookup_key=lookup_key, transfer_lookup_key=True,
        )
        print(f"  created price {lookup_key} = ${amount/100:.2f}")
    else:
        print(f"  price {lookup_key} ok")


def main():
    ensure_tax_settings()
    for entry in CATALOG:
        print(f"Product: {entry['name']}")
        product = get_or_create_product(entry)
        ensure_price(product, entry)
    for entry in BUNDLES:
        print(f"Bundle: {entry['name']}")
        product = get_or_create_product(entry)
        ensure_price(product, entry)
    print("Done. Catalog + bundles synced to Stripe.")


if __name__ == "__main__":
    main()
