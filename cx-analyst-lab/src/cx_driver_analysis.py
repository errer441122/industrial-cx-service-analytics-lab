"""Statistical CX driver analysis on top of the feedback sample.

Goes past a single bivariate cut: every categorical level is tested against
its complement with a two-proportion z-test, Cohen's *h* effect size and a
95% confidence interval, so weak-but-significant and strong-but-noisy effects
are told apart. A follow-up cohort comparison gives an observational read on
whether completing follow-ups moves the post-action outcome, and a keyword
pass surfaces the dominant friction themes from free-text comments.

Pure standard library (``math``/``statistics``) so it runs anywhere the
validator runs, with no numerical-stack version risk.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

from validate_cx_data import DATA_PATH, load_rows, validate_rows

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
METRICS_PATH = REPORTS_DIR / "cx_driver_metrics.json"
REPORT_PATH = REPORTS_DIR / "cx_driver_analysis.md"

SATISFIED_MIN = 4  # satisfaction_score 4 or 5 counts as "satisfied"
Z_95 = 1.959963984540054

THEME_LEXICON = {
    "Financing & pricing": ["financ", "price", "pricing", "cost", "trade-in", "valuation"],
    "Documentation & warranty": ["document", "warranty", "insurance", "registration", "recall"],
    "Digital onboarding": ["app", "onboard", "connectivity", "pairing", "account", "login"],
    "Service & parts": ["parts", "appointment", "wait", "repair", "maintenance", "turnaround"],
    "Delivery & handover": ["delivery", "handover", "test ride", "order tracking"],
}


def _norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def two_proportion_z(s1: int, n1: int, s2: int, n2: int) -> dict[str, float]:
    """Pooled two-proportion z-test plus Cohen's h and a Wald CI on the gap."""
    if n1 == 0 or n2 == 0:
        return {"p1": 0.0, "p2": 0.0, "diff": 0.0, "z": 0.0, "p_value": 1.0,
                "cohens_h": 0.0, "ci_low": 0.0, "ci_high": 0.0}
    p1, p2 = s1 / n1, s2 / n2
    pooled = (s1 + s2) / (n1 + n2)
    se_pool = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se_pool if se_pool > 0 else 0.0
    p_value = 2.0 * (1.0 - _norm_cdf(abs(z)))
    h = 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))
    se_unpooled = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return {
        "p1": round(p1, 4),
        "p2": round(p2, 4),
        "diff": round(p1 - p2, 4),
        "z": round(z, 3),
        "p_value": round(p_value, 5),
        "cohens_h": round(h, 3),
        "ci_low": round((p1 - p2) - Z_95 * se_unpooled, 4),
        "ci_high": round((p1 - p2) + Z_95 * se_unpooled, 4),
    }


def wilson_ci(successes: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    z2 = Z_95 * Z_95
    denom = 1 + z2 / n
    centre = (p + z2 / (2 * n)) / denom
    half = (Z_95 * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))) / denom
    return (round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4))


def _effect_label(h: float) -> str:
    a = abs(h)
    if a < 0.2:
        return "negligible"
    if a < 0.5:
        return "small"
    if a < 0.8:
        return "medium"
    return "large"


def _satisfied(row: dict[str, str]) -> bool:
    return int(row["satisfaction_score"]) >= SATISFIED_MIN


def driver_table(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Each categorical level vs its complement, ranked by |effect size|."""
    total_sat = sum(1 for r in rows if _satisfied(r))
    total_n = len(rows)
    results: list[dict[str, object]] = []

    dimensions = ["segment", "journey_stage", "region", "channel"]
    for dim in dimensions:
        for level in sorted({r[dim] for r in rows}):
            in_rows = [r for r in rows if r[dim] == level]
            s1 = sum(1 for r in in_rows if _satisfied(r))
            n1 = len(in_rows)
            s2, n2 = total_sat - s1, total_n - n1
            test = two_proportion_z(s1, n1, s2, n2)
            lo, hi = wilson_ci(s1, n1)
            results.append({
                "dimension": dim,
                "level": level,
                "n": n1,
                "satisfied_rate": test["p1"],
                "satisfied_ci": [lo, hi],
                "rest_rate": test["p2"],
                "diff_vs_rest": test["diff"],
                "diff_ci": [test["ci_low"], test["ci_high"]],
                "z": test["z"],
                "p_value": test["p_value"],
                "cohens_h": test["cohens_h"],
                "effect": _effect_label(test["cohens_h"]),
                "significant": test["p_value"] < 0.05,
            })

    # Friction is the strongest single lever; test high (>=4) vs the rest.
    high = [r for r in rows if int(r["friction_score"]) >= 4]
    sH, nH = sum(1 for r in high if _satisfied(r)), len(high)
    test = two_proportion_z(sH, nH, total_sat - sH, total_n - nH)
    lo, hi = wilson_ci(sH, nH)
    results.append({
        "dimension": "friction_score",
        "level": "high (>=4)",
        "n": nH,
        "satisfied_rate": test["p1"],
        "satisfied_ci": [lo, hi],
        "rest_rate": test["p2"],
        "diff_vs_rest": test["diff"],
        "diff_ci": [test["ci_low"], test["ci_high"]],
        "z": test["z"],
        "p_value": test["p_value"],
        "cohens_h": test["cohens_h"],
        "effect": _effect_label(test["cohens_h"]),
        "significant": test["p_value"] < 0.05,
    })

    results.sort(key=lambda r: abs(r["cohens_h"]), reverse=True)
    return results


def follow_up_cohort(rows: list[dict[str, str]]) -> dict[str, object]:
    """Observational read: did completing a required follow-up move outcomes?"""
    required = [r for r in rows if r["follow_up_required"].lower() == "yes"]
    done = [r for r in required if r["follow_up_completed"].lower() == "yes"]
    open_ = [r for r in required if r["follow_up_completed"].lower() == "no"]

    def post_satisfied(rs: list[dict[str, str]]) -> int:
        return sum(1 for r in rs if int(r["post_action_score"]) >= SATISFIED_MIN)

    sD, nD = post_satisfied(done), len(done)
    sO, nO = post_satisfied(open_), len(open_)
    test = two_proportion_z(sD, nD, sO, nO)

    def mean_delta(rs: list[dict[str, str]]) -> float:
        if not rs:
            return 0.0
        return round(
            sum(int(r["post_action_score"]) - int(r["satisfaction_score"]) for r in rs) / len(rs), 3
        )

    return {
        "required_n": len(required),
        "completed_n": nD,
        "open_n": nO,
        "completed_post_satisfied_rate": test["p1"],
        "open_post_satisfied_rate": test["p2"],
        "rate_gap": test["diff"],
        "rate_gap_ci": [test["ci_low"], test["ci_high"]],
        "z": test["z"],
        "p_value": test["p_value"],
        "cohens_h": test["cohens_h"],
        "effect": _effect_label(test["cohens_h"]),
        "completed_mean_delta": mean_delta(done),
        "open_mean_delta": mean_delta(open_),
        "significant": test["p_value"] < 0.05,
    }


def comment_themes(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    counts: Counter[str] = Counter()
    sat_sum: dict[str, int] = defaultdict(int)
    for row in rows:
        text = row["comment"].lower()
        for theme, keywords in THEME_LEXICON.items():
            if any(re.search(re.escape(k), text) for k in keywords):
                counts[theme] += 1
                sat_sum[theme] += int(row["satisfaction_score"])
    out = []
    for theme, n in counts.most_common():
        out.append({
            "theme": theme,
            "mentions": n,
            "share": round(n / len(rows), 3),
            "avg_satisfaction": round(sat_sum[theme] / n, 2),
        })
    return out


def run(rows: list[dict[str, str]] | None = None) -> dict[str, object]:
    rows = rows if rows is not None else load_rows(DATA_PATH)
    errors = validate_rows(rows)
    if errors:
        raise ValueError("; ".join(errors))

    total_sat = sum(1 for r in rows if _satisfied(r))
    lo, hi = wilson_ci(total_sat, len(rows))
    drivers = driver_table(rows)
    # friction_score is reported as the *mechanism*, not a targetable cohort
    # (high friction is near-definitionally low satisfaction). The actionable
    # headline is the strongest significant cut on a population dimension.
    actionable = [d for d in drivers if d["dimension"] != "friction_score"]
    return {
        "records": len(rows),
        "overall_satisfied_rate": round(total_sat / len(rows), 4),
        "overall_satisfied_ci_95": [lo, hi],
        "drivers": drivers,
        "top_negative_driver": next(
            (d for d in actionable if d["diff_vs_rest"] < 0 and d["significant"]), None
        ),
        "strongest_mechanism": next(
            (d for d in drivers if d["dimension"] == "friction_score"), None
        ),
        "follow_up_cohort": follow_up_cohort(rows),
        "comment_themes": comment_themes(rows),
    }


def _fmt_pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def write_reports(result: dict[str, object]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    drivers = result["drivers"]
    top = result["top_negative_driver"]
    coh = result["follow_up_cohort"]
    lo, hi = result["overall_satisfied_ci_95"]

    lines = []
    lines.append("# CX Driver Analysis\n")
    lines.append(
        f"Sample: **{result['records']} synthetic feedback records**. Overall satisfied "
        f"rate (score 4-5) **{_fmt_pct(result['overall_satisfied_rate'])}** "
        f"(95% CI {_fmt_pct(lo)}-{_fmt_pct(hi)}, Wilson).\n"
    )
    lines.append("## Driver ranking (level vs the rest)\n")
    lines.append(
        "Two-proportion z-test on the satisfied rate, Cohen's *h* effect size, "
        "95% Wald CI on the gap. Ranked by |effect|.\n"
    )
    lines.append("| Dimension | Level | n | Satisfied | Δ vs rest | 95% CI (Δ) | Cohen's h | p | Effect |")
    lines.append("| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |")
    for d in drivers:
        flag = "" if d["significant"] else " (n.s.)"
        lines.append(
            f"| {d['dimension']} | {d['level']} | {d['n']} | {_fmt_pct(d['satisfied_rate'])} | "
            f"{d['diff_vs_rest']:+.3f} | [{d['diff_ci'][0]:+.3f}, {d['diff_ci'][1]:+.3f}] | "
            f"{d['cohens_h']:+.2f} | {d['p_value']:.4f}{flag} | {d['effect']} |"
        )
    lines.append("")

    if top:
        lines.append(
            f"**Strongest actionable at-risk cut:** `{top['dimension']} = {top['level']}` — "
            f"satisfied rate {_fmt_pct(top['satisfied_rate'])} vs {_fmt_pct(top['rest_rate'])} for "
            f"the rest (Δ {top['diff_vs_rest']:+.1%}, Cohen's h {top['cohens_h']:+.2f}, "
            f"{top['effect']} effect, p = {top['p_value']:.4f}). This is a population segment "
            f"operations can target.\n"
        )
    mech = result.get("strongest_mechanism")
    if mech:
        lines.append(
            f"_Mechanism (not a targetable cohort): records with friction score >=4 sit at "
            f"{_fmt_pct(mech['satisfied_rate'])} satisfied vs {_fmt_pct(mech['rest_rate'])} "
            f"(Cohen's h {mech['cohens_h']:+.2f}). Friction is near-definitionally tied to "
            f"satisfaction; it is the lever, the segment cut is where to pull it._\n"
        )

    lines.append("## Follow-up cohort (observational)\n")
    sig = "significant" if coh["significant"] else "not significant"
    lines.append(
        f"Among {coh['required_n']} records needing follow-up, {coh['completed_n']} were "
        f"completed and {coh['open_n']} left open. Post-action satisfied rate is "
        f"**{_fmt_pct(coh['completed_post_satisfied_rate'])}** for completed vs "
        f"**{_fmt_pct(coh['open_post_satisfied_rate'])}** for open "
        f"(gap {coh['rate_gap']:+.1%}, 95% CI [{coh['rate_gap_ci'][0]:+.3f}, "
        f"{coh['rate_gap_ci'][1]:+.3f}], Cohen's h {coh['cohens_h']:+.2f}, "
        f"{coh['effect']} effect, p = {coh['p_value']:.4f}, {sig}). Mean score change: "
        f"{coh['completed_mean_delta']:+.2f} completed vs {coh['open_mean_delta']:+.2f} open.\n"
    )
    lines.append(
        "_This is an observational cohort split, not a randomized test: records that "
        "get a completed follow-up may differ systematically from those that do not._\n"
    )

    lines.append("## Comment themes\n")
    lines.append("| Theme | Mentions | Share | Avg satisfaction |")
    lines.append("| --- | ---: | ---: | ---: |")
    for t in result["comment_themes"]:
        lines.append(
            f"| {t['theme']} | {t['mentions']} | {_fmt_pct(t['share'])} | {t['avg_satisfaction']:.2f} |"
        )
    lines.append("")
    lines.append("## Boundary\n")
    lines.append(
        "Data is synthetic with a disclosed generative model "
        "(`data/cx_dataset_card.md`); these statistics quantify how cleanly the "
        "pipeline recovers an injected structure and are evidence of analytical "
        "discipline, not real-world customer truth. All relationships are "
        "observational, not causal.\n"
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    result = run()
    write_reports(result)
    print(f"Wrote {METRICS_PATH.relative_to(ROOT)} and {REPORT_PATH.relative_to(ROOT)}")
    top = result["top_negative_driver"]
    if top:
        print(
            f"Top at-risk driver: {top['dimension']}={top['level']} "
            f"(h={top['cohens_h']:+.2f}, p={top['p_value']:.4f})"
        )


if __name__ == "__main__":
    main()
