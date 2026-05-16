"""Prepare a committable CX dataset from the **real** public *Olist
Brazilian E-Commerce* dataset.

Source : Kaggle — olistbr/brazilian-ecommerce
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0
         International (CC BY-NC-SA 4.0). Used here for a **non-commercial**
         job-application portfolio, with attribution and share-alike.

Olist needs a Kaggle login to download, so this script does NOT fetch it:
place the downloaded archive at `.cache/olist.zip` (git-ignored). The
script verifies its SHA256, then joins reviews + orders + customers +
order items + product categories into two committable CSVs:

- `data/olist_reviews.csv`        — one row per review, structured features
  (score, satisfaction, NPS-proxy band, state, category, delivery timing,
  freight ratio). Real values, BRL currency.
- `data/olist_review_comments.csv` — review_id + the Portuguese comment
  text, for the comment-theme analysis (kept separate to bound size).

Cleaning rules (documented): keep reviews whose order is `delivered` with
a valid purchase and customer-delivery date (so delivery metrics are
defined); one row per review_id; order-level price/freight summed across
items; product category from the order's first item, English-translated.

Pure standard library.
"""

from __future__ import annotations

import csv
import hashlib
import sys
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".cache"
SOURCE_ZIP = CACHE_DIR / "olist.zip"
OUT_REVIEWS = ROOT / "data" / "olist_reviews.csv"
OUT_COMMENTS = ROOT / "data" / "olist_review_comments.csv"
PROVENANCE = ROOT / "data" / "REAL_DATA_PROVENANCE.md"

SRC_ZIP_SHA256 = "967e41e04fc306fe604e2a693f488995a8b41e5047418f8a5c8e4abd6deca784"
NEEDED = [
    "olist_orders_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_products_dataset.csv",
    "product_category_name_translation.csv",
]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_source() -> None:
    if not SOURCE_ZIP.exists():
        sys.exit(
            "Missing .cache/olist.zip. Olist requires a Kaggle login; "
            "download 'olistbr/brazilian-ecommerce' and save the archive as "
            f"{SOURCE_ZIP} (git-ignored), then re-run."
        )
    digest = _sha256(SOURCE_ZIP)
    if digest != SRC_ZIP_SHA256:
        sys.exit(f"olist.zip checksum mismatch: expected {SRC_ZIP_SHA256}, got {digest}")
    with zipfile.ZipFile(SOURCE_ZIP) as zf:
        for name in NEEDED:
            zf.extract(name, CACHE_DIR)


def _read(name: str) -> list[dict[str, str]]:
    # utf-8-sig strips the UTF-8 BOM present on some Olist headers.
    with (CACHE_DIR / name).open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _date(s: str):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(s[:10], "%Y-%m-%d")
        except ValueError:
            return None


def build():
    customers = {r["customer_id"]: r["customer_state"] for r in _read("olist_customers_dataset.csv")}
    cat_en = {
        r["product_category_name"]: r["product_category_name_english"]
        for r in _read("product_category_name_translation.csv")
    }
    prod_cat = {
        r["product_id"]: cat_en.get(r["product_category_name"], r["product_category_name"] or "unknown")
        for r in _read("olist_products_dataset.csv")
    }

    order_price: dict[str, float] = defaultdict(float)
    order_freight: dict[str, float] = defaultdict(float)
    order_first_cat: dict[str, str] = {}
    for it in _read("olist_order_items_dataset.csv"):
        oid = it["order_id"]
        order_price[oid] += float(it["price"] or 0)
        order_freight[oid] += float(it["freight_value"] or 0)
        if it["order_item_id"] == "1":
            order_first_cat[oid] = prod_cat.get(it["product_id"], "unknown")

    orders = {}
    for o in _read("olist_orders_dataset.csv"):
        orders[o["order_id"]] = {
            "customer_id": o["customer_id"],
            "status": o["order_status"],
            "purchase": _date(o["order_purchase_timestamp"]),
            "delivered": _date(o["order_delivered_customer_date"]),
            "estimated": _date(o["order_estimated_delivery_date"]),
        }

    reviews_out: list[dict[str, object]] = []
    comments_out: list[dict[str, object]] = []
    seen: set[str] = set()
    raw = 0
    for rv in _read("olist_order_reviews_dataset.csv"):
        raw += 1
        rid = rv["review_id"]
        oid = rv["order_id"]
        if rid in seen:
            continue
        o = orders.get(oid)
        if not o or o["status"] != "delivered" or not o["purchase"] or not o["delivered"] or not o["estimated"]:
            continue
        try:
            score = int(rv["review_score"])
        except (TypeError, ValueError):
            continue
        seen.add(rid)

        delivery_days = (o["delivered"] - o["purchase"]).days
        estimated_days = (o["estimated"] - o["purchase"]).days
        delay = (o["delivered"] - o["estimated"]).days
        price = round(order_price.get(oid, 0.0), 2)
        freight = round(order_freight.get(oid, 0.0), 2)
        denom = price + freight
        comment = " ".join((rv.get("review_comment_message") or "").split()).strip()

        reviews_out.append({
            "review_id": rid,
            "order_id": oid,
            "review_score": score,
            "purchase_month": o["purchase"].strftime("%Y-%m"),
            "satisfied": 1 if score >= 4 else 0,
            "nps_band": "promoter" if score == 5 else "passive" if score == 4 else "detractor",
            "customer_state": customers.get(o["customer_id"], "NA"),
            "product_category": order_first_cat.get(oid, "unknown"),
            "delivery_days": delivery_days,
            "estimated_days": estimated_days,
            "delivery_delay_days": delay,
            "late_delivery": 1 if delay > 0 else 0,
            "total_price_brl": price,
            "total_freight_brl": freight,
            "freight_ratio": round(freight / denom, 4) if denom > 0 else 0.0,
            "has_comment": 1 if comment else 0,
            "comment_len": len(comment),
        })
        if comment:
            comments_out.append({"review_id": rid, "comment": comment})

    reviews_out.sort(key=lambda r: r["review_id"])
    comments_out.sort(key=lambda r: r["review_id"])
    return reviews_out, comments_out, raw


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_provenance(reviews, comments, raw) -> None:
    states = len({r["customer_state"] for r in reviews})
    cats = len({r["product_category"] for r in reviews})
    sat = sum(r["satisfied"] for r in reviews) / len(reviews)
    PROVENANCE.write_text(
        f"""# Real Data Provenance

## Source

- **Dataset:** Olist Brazilian E-Commerce Public Dataset
- **Origin:** Kaggle — `olistbr/brazilian-ecommerce`
- **License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0
  International (**CC BY-NC-SA 4.0**). This portfolio is **non-commercial**;
  the dataset is attributed and not redistributed beyond the prepared,
  transformed extract used for analysis.
- **Source archive SHA256:** `{SRC_ZIP_SHA256}`
- **Status:** REAL public e-commerce data (Brazil, 2016-2018). Not simulated.
- **Currency:** Brazilian Real (BRL), reported as such (not EUR).

## Cleaning rules

1. Keep reviews whose order status is `delivered` with valid purchase and
   customer-delivery dates (so delivery metrics are well defined).
2. One row per `review_id`.
3. Order-level price and freight summed across order items; product
   category from the order's first item, English-translated.
4. NPS band is a **disclosed proxy** from the 1-5 review score
   (5 = promoter, 4 = passive, ≤ 3 = detractor) — Olist has no 0-10
   likelihood-to-recommend question.

## Prepared sample

- `data/olist_reviews.csv` — {len(reviews):,} reviews, {states} states,
  {cats} product categories, satisfied rate {sat:.1%}.
- `data/olist_review_comments.csv` — {len(comments):,} Portuguese review
  comments (review_id keyed).
- Raw review rows scanned: {raw:,}.

SHA256 of the committed files (LF line endings):

- olist_reviews.csv: `{_sha256(OUT_REVIEWS)}`
- olist_review_comments.csv: `{_sha256(OUT_COMMENTS)}`

Re-running `python src/prepare_real_data.py` reproduces both files
byte-for-byte from the SHA256-pinned source.

## Note

This CX lab is now **fully real** — there is no synthetic data. The only
disclosed approximation is the NPS *band* proxy above (a relabelling of the
real review score, not invented data).
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_source()
    reviews, comments, raw = build()
    _write_csv(OUT_REVIEWS, reviews)
    _write_csv(OUT_COMMENTS, comments)
    write_provenance(reviews, comments, raw)
    print(
        f"Wrote {len(reviews):,} real reviews ({len(comments):,} with "
        f"comments) from Olist to data/ (raw scanned {raw:,})."
    )


if __name__ == "__main__":
    main()
