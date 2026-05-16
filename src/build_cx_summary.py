"""Stakeholder CX summary on the real Olist reviews dataset.

A compact, decision-oriented readout (headline KPIs, NPS proxy, the
delivery-SLA signal, and a monthly trend) built from
`data/olist_reviews.csv`. Pure standard library.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from cx_driver_analysis import load_reviews

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
BRIEF_PATH = REPORTS_DIR / "customer_satisfaction_brief.md"

MIN_GROUP = 400


def build_summary(rows: list[dict[str, object]] | None = None) -> dict[str, object]:
    rows = rows if rows is not None else load_reviews()
    n = len(rows)
    sat = sum(r["satisfied"] for r in rows)
    prom = sum(1 for r in rows if r["nps_band"] == "promoter")
    det = sum(1 for r in rows if r["nps_band"] == "detractor")
    late = sum(r["late"] for r in rows)
    dd = sorted(r["delivery_days"] for r in rows)

    def grp(field: str) -> dict[str, dict[str, object]]:
        g: dict[str, list[dict[str, object]]] = defaultdict(list)
        for r in rows:
            g[r[field]].append(r)
        out = {}
        for k, rs in g.items():
            if len(rs) >= MIN_GROUP:
                out[k] = {
                    "reviews": len(rs),
                    "satisfied_rate": round(sum(x["satisfied"] for x in rs) / len(rs), 4),
                    "avg_review_score": round(sum(x["score"] for x in rs) / len(rs), 2),
                    "late_rate": round(sum(x["late"] for x in rs) / len(rs), 4),
                }
        return dict(sorted(out.items(), key=lambda kv: kv[1]["satisfied_rate"]))

    months = defaultdict(list)
    for r in rows:
        months[r["month"]].append(r)
    monthly_trend = {
        m: {
            "reviews": len(rs),
            "satisfied_rate": round(sum(x["satisfied"] for x in rs) / len(rs), 4),
            "avg_review_score": round(sum(x["score"] for x in rs) / len(rs), 2),
            "late_rate": round(sum(x["late"] for x in rs) / len(rs), 4),
        }
        for m, rs in sorted(months.items())
    }

    return {
        "dataset": "Olist Brazilian E-Commerce (real, CC BY-NC-SA 4.0)",
        "records": n,
        "customer_satisfaction_rate": round(sat / n, 4),
        "customer_satisfaction_rate_pct": round(sat / n * 100, 1),
        "avg_review_score": round(sum(r["score"] for r in rows) / n, 3),
        "nps_proxy": round((prom - det) / n * 100, 1),
        "late_delivery_rate": round(late / n, 4),
        "median_delivery_days": dd[len(dd) // 2],
        "by_state": grp("state"),
        "by_category": grp("category"),
        "monthly_trend": monthly_trend,
    }


def _md(s: dict[str, object]) -> str:
    L = ["# Customer Satisfaction Brief (real Olist data)\n"]
    L.append(
        f"{s['records']:,} real reviews — satisfied **{s['customer_satisfaction_rate_pct']}%**, "
        f"avg score **{s['avg_review_score']}**, NPS proxy **{s['nps_proxy']:+.0f}**, "
        f"late-delivery rate **{s['late_delivery_rate']*100:.1f}%**, median delivery "
        f"**{s['median_delivery_days']} days**.\n"
    )
    L.append("## Lowest-satisfaction states (≥ %d reviews)\n" % MIN_GROUP)
    L.append("| State | Reviews | Satisfied | Avg score | Late rate |")
    L.append("| --- | ---: | ---: | ---: | ---: |")
    for st, m in list(s["by_state"].items())[:8]:
        L.append(f"| {st} | {m['reviews']:,} | {m['satisfied_rate']*100:.1f}% | "
                 f"{m['avg_review_score']} | {m['late_rate']*100:.1f}% |")
    L.append("")
    L.append("## Lowest-satisfaction categories (≥ %d reviews)\n" % MIN_GROUP)
    L.append("| Category | Reviews | Satisfied | Avg score | Late rate |")
    L.append("| --- | ---: | ---: | ---: | ---: |")
    for c, m in list(s["by_category"].items())[:8]:
        L.append(f"| {c} | {m['reviews']:,} | {m['satisfied_rate']*100:.1f}% | "
                 f"{m['avg_review_score']} | {m['late_rate']*100:.1f}% |")
    L.append("")
    L.append(
        "Takeaway: satisfaction tracks delivery reliability. The priority is "
        "cutting late deliveries in the weakest states/categories, not broad "
        "review solicitation — see `cx_driver_analysis.md`.\n"
    )
    L.append("## Boundary\n")
    L.append(
        "Real public data (Olist, Kaggle, CC BY-NC-SA 4.0, non-commercial, "
        "attributed). Observational, not causal; Brazil 2016-2018.\n"
    )
    return "\n".join(L)


def main() -> None:
    summary = build_summary()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    BRIEF_PATH.write_text(_md(summary), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("by_state", "by_category", "monthly_trend")},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
