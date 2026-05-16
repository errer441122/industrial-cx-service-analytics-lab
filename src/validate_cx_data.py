"""Validate the prepared **real** Olist CX extract.

Checks `data/olist_reviews.csv` (schema, ranges, internal consistency) and
`data/olist_review_comments.csv` (keyed to real reviews). Pure standard
library; exits non-zero on any violation so CI fails loudly.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS_PATH = ROOT / "data" / "olist_reviews.csv"
COMMENTS_PATH = ROOT / "data" / "olist_review_comments.csv"

REVIEW_COLUMNS = {
    "review_id", "order_id", "review_score", "purchase_month", "satisfied",
    "nps_band", "customer_state", "product_category", "delivery_days",
    "estimated_days", "delivery_delay_days", "late_delivery",
    "total_price_brl", "total_freight_brl", "freight_ratio",
    "has_comment", "comment_len",
}
NPS_BANDS = {"promoter", "passive", "detractor"}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def validate_reviews(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    if not rows:
        return ["olist_reviews.csv has no rows"]
    missing = REVIEW_COLUMNS - set(rows[0])
    if missing:
        return [f"missing columns: {sorted(missing)}"]
    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        rid = r["review_id"]
        if not rid:
            errors.append(f"line {i}: empty review_id")
        if rid in seen:
            errors.append(f"line {i}: duplicate review_id {rid}")
        seen.add(rid)
        score = int(r["review_score"])
        if not 1 <= score <= 5:
            errors.append(f"line {i}: review_score out of range")
        if r["satisfied"] not in ("0", "1"):
            errors.append(f"line {i}: satisfied must be 0/1")
        if (score >= 4) != (r["satisfied"] == "1"):
            errors.append(f"line {i}: satisfied inconsistent with score")
        if r["nps_band"] not in NPS_BANDS:
            errors.append(f"line {i}: bad nps_band")
        if r["late_delivery"] not in ("0", "1"):
            errors.append(f"line {i}: late_delivery must be 0/1")
        if (int(r["delivery_delay_days"]) > 0) != (r["late_delivery"] == "1"):
            errors.append(f"line {i}: late_delivery inconsistent with delay")
        if not 0.0 <= float(r["freight_ratio"]) <= 1.0:
            errors.append(f"line {i}: freight_ratio out of [0,1]")
        if float(r["total_price_brl"]) < 0 or float(r["total_freight_brl"]) < 0:
            errors.append(f"line {i}: negative monetary value")
        if len(r["purchase_month"]) != 7 or r["purchase_month"][4] != "-":
            errors.append(f"line {i}: purchase_month not YYYY-MM")
    if len(rows) < 1000:
        errors.append("expected a substantial real sample (>= 1000 reviews)")
    return errors


def validate_comments(comments: list[dict[str, str]], review_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if comments and set(comments[0]) != {"review_id", "comment"}:
        errors.append(f"comments columns unexpected: {sorted(comments[0])}")
    for i, c in enumerate(comments, start=2):
        if not c["review_id"]:
            errors.append(f"comments line {i}: empty review_id")
        elif c["review_id"] not in review_ids:
            errors.append(f"comments line {i}: review_id not in reviews")
        if not c["comment"].strip():
            errors.append(f"comments line {i}: empty comment")
    return errors


def validate_file() -> list[str]:
    reviews = _read(REVIEWS_PATH)
    errors = validate_reviews(reviews)
    if not errors and COMMENTS_PATH.exists():
        ids = {r["review_id"] for r in reviews}
        errors += validate_comments(_read(COMMENTS_PATH), ids)
    return errors


def main() -> None:
    errors = validate_file()
    if errors:
        raise SystemExit("CX data validation failed:\n- " + "\n- ".join(errors[:20]))
    print("CX real data validation passed.")


if __name__ == "__main__":
    main()
