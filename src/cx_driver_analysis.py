"""Statistical CX driver analysis on the **real** Olist dataset.

Input: `data/olist_reviews.csv` (prepared by `prepare_real_data.py` from the
Kaggle Olist Brazilian E-Commerce dataset, CC BY-NC-SA 4.0; see
`data/REAL_DATA_PROVENANCE.md`). Real values, BRL currency, 2016-2018.

What it produces:
- overall satisfied rate (review score 4-5) with a Wilson 95% CI;
- **NPS** from the disclosed score→band proxy, overall and by state;
- a **driver ranking**: every categorical level vs its complement with a
  two-proportion z-test, Cohen's *h* and a 95% CI, ranked by |effect|;
- the **late-delivery mechanism** (late vs on-time), the strongest real
  lever on satisfaction;
- a **delivery-SLA cohort** (on-time vs late) — the real analogue of an
  intervention read;
- **comment themes** from a disclosed Portuguese keyword lexicon;
- a **multivariate logistic regression** for P(satisfied) so each driver is
  read controlling for the others.

Pure standard library.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS_PATH = ROOT / "data" / "olist_reviews.csv"
COMMENTS_PATH = ROOT / "data" / "olist_review_comments.csv"
REPORTS_DIR = ROOT / "reports"
METRICS_PATH = REPORTS_DIR / "cx_driver_metrics.json"
REPORT_PATH = REPORTS_DIR / "cx_driver_analysis.md"

Z_95 = 1.959963984540054
MIN_GROUP = 400  # don't rank a state/category level below this many reviews
TOP_STATES = 6
TOP_CATEGORIES = 8

# Disclosed Portuguese keyword lexicon (substring match, accent-naive).
THEME_LEXICON = {
    "Entrega & prazo": ["entrega", "prazo", "atras", "chegou", "demor", "antes do prazo", "rapid"],
    "Produto & qualidade": ["produto", "qualidade", "defeit", "quebrad", "danific", "origin"],
    "Não recebido / faltou": ["nao recebi", "não recebi", "nao chegou", "não chegou", "faltou", "faltando"],
    "Recomendação / satisfação": ["recomend", "satisfeit", "gostei", "otimo", "ótimo", "excelente"],
    "Atendimento": ["atendimento", "contato", "resposta", "suporte", "reembolso", "troca"],
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
        "p1": round(p1, 4), "p2": round(p2, 4), "diff": round(p1 - p2, 4),
        "z": round(z, 3), "p_value": round(p_value, 6), "cohens_h": round(h, 3),
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


def _effect(h: float) -> str:
    a = abs(h)
    return "negligible" if a < 0.2 else "small" if a < 0.5 else "medium" if a < 0.8 else "large"


def load_reviews() -> list[dict[str, object]]:
    out = []
    with REVIEWS_PATH.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.append({
                "review_id": r["review_id"],
                "score": int(r["review_score"]),
                "satisfied": int(r["satisfied"]),
                "nps_band": r["nps_band"],
                "state": r["customer_state"],
                "category": r["product_category"],
                "delivery_days": int(r["delivery_days"]),
                "delay": int(r["delivery_delay_days"]),
                "late": int(r["late_delivery"]),
                "freight_ratio": float(r["freight_ratio"]),
                "month": r["purchase_month"],
            })
    return out


def _speed_bucket(days: int) -> str:
    return "fast (≤7d)" if days <= 7 else "normal (8-14d)" if days <= 14 else "slow (15d+)"


def _freight_bucket(fr: float) -> str:
    return "low freight" if fr < 0.12 else "mid freight" if fr < 0.22 else "high freight"


def nps_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    def score(rs: list[dict[str, object]]) -> dict[str, object]:
        n = len(rs)
        if n == 0:
            return {"n": 0, "nps": 0.0}
        prom = sum(1 for r in rs if r["nps_band"] == "promoter")
        det = sum(1 for r in rs if r["nps_band"] == "detractor")
        p_p, p_d = prom / n, det / n
        nps = (p_p - p_d) * 100
        var = (p_p + p_d - (p_p - p_d) ** 2) / n
        half = Z_95 * math.sqrt(max(var, 0.0)) * 100
        return {"n": n, "promoters": prom, "detractors": det,
                "nps": round(nps, 1), "nps_ci_95": [round(nps - half, 1), round(nps + half, 1)]}

    overall = score(rows)
    counts = Counter(r["state"] for r in rows)
    by_state = []
    for st in [s for s, c in counts.most_common() if c >= MIN_GROUP]:
        s = score([r for r in rows if r["state"] == st])
        s["state"] = st
        by_state.append(s)
    by_state.sort(key=lambda r: r["nps"])
    return {"overall": overall, "by_state": by_state, "proxy": "score 5=promoter, 4=passive, ≤3=detractor"}


def driver_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    total_sat = sum(r["satisfied"] for r in rows)
    total_n = len(rows)
    results: list[dict[str, object]] = []

    def add(dim: str, level: str, members: list[dict[str, object]]) -> None:
        n1 = len(members)
        if n1 < MIN_GROUP:
            return
        s1 = sum(r["satisfied"] for r in members)
        t = two_proportion_z(s1, n1, total_sat - s1, total_n - n1)
        lo, hi = wilson_ci(s1, n1)
        results.append({
            "dimension": dim, "level": level, "n": n1,
            "satisfied_rate": t["p1"], "satisfied_ci": [lo, hi],
            "rest_rate": t["p2"], "diff_vs_rest": t["diff"],
            "diff_ci": [t["ci_low"], t["ci_high"]], "z": t["z"],
            "p_value": t["p_value"], "cohens_h": t["cohens_h"],
            "effect": _effect(t["cohens_h"]), "significant": t["p_value"] < 0.05,
        })

    top_states = [s for s, _ in Counter(r["state"] for r in rows).most_common(TOP_STATES)]
    for st in sorted(top_states):
        add("customer_state", st, [r for r in rows if r["state"] == st])
    top_cats = [c for c, _ in Counter(r["category"] for r in rows).most_common(TOP_CATEGORIES)]
    for c in sorted(top_cats):
        add("product_category", c, [r for r in rows if r["category"] == c])
    for b in ("fast (≤7d)", "normal (8-14d)", "slow (15d+)"):
        add("delivery_speed", b, [r for r in rows if _speed_bucket(r["delivery_days"]) == b])
    for b in ("low freight", "mid freight", "high freight"):
        add("freight_level", b, [r for r in rows if _freight_bucket(r["freight_ratio"]) == b])
    add("late_delivery", "late (delivered after estimate)", [r for r in rows if r["late"] == 1])

    results.sort(key=lambda r: abs(r["cohens_h"]), reverse=True)
    return results


def delivery_sla_cohort(rows: list[dict[str, object]]) -> dict[str, object]:
    """Real analogue of an intervention read: on-time vs late delivery."""
    on_time = [r for r in rows if r["late"] == 0]
    late = [r for r in rows if r["late"] == 1]
    sO, nO = sum(r["satisfied"] for r in on_time), len(on_time)
    sL, nL = sum(r["satisfied"] for r in late), len(late)
    t = two_proportion_z(sO, nO, sL, nL)

    def mean_score(rs):
        return round(sum(r["score"] for r in rs) / len(rs), 3) if rs else 0.0

    return {
        "on_time_n": nO, "late_n": nL,
        "on_time_satisfied_rate": t["p1"], "late_satisfied_rate": t["p2"],
        "rate_gap": t["diff"], "rate_gap_ci": [t["ci_low"], t["ci_high"]],
        "z": t["z"], "p_value": t["p_value"], "cohens_h": t["cohens_h"],
        "effect": _effect(t["cohens_h"]), "significant": t["p_value"] < 0.05,
        "on_time_mean_score": mean_score(on_time), "late_mean_score": mean_score(late),
    }


def comment_themes(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    score_by_id = {r["review_id"]: r["score"] for r in rows}
    counts: Counter[str] = Counter()
    score_sum: dict[str, int] = defaultdict(int)
    n_comments = 0
    if COMMENTS_PATH.exists():
        with COMMENTS_PATH.open(newline="", encoding="utf-8") as fh:
            for c in csv.DictReader(fh):
                rid = c["review_id"]
                if rid not in score_by_id:
                    continue
                n_comments += 1
                text = c["comment"].lower()
                for theme, kws in THEME_LEXICON.items():
                    if any(k in text for k in kws):
                        counts[theme] += 1
                        score_sum[theme] += score_by_id[rid]
    out = []
    for theme, n in counts.most_common():
        out.append({"theme": theme, "mentions": n,
                     "share_of_comments": round(n / n_comments, 4) if n_comments else 0.0,
                     "avg_review_score": round(score_sum[theme] / n, 2)})
    return out


def _matrix_inverse(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[piv] = aug[piv], aug[col]
        d = aug[col][col] or 1e-12
        aug[col] = [v / d for v in aug[col]]
        for r in range(n):
            if r != col:
                f = aug[r][col]
                aug[r] = [a - f * b for a, b in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]


def logistic_drivers(rows: list[dict[str, object]]) -> dict[str, object]:
    """Multivariate logistic regression for P(satisfied), controlling for the
    other drivers. Ridge-penalised Newton-Raphson, pure stdlib."""
    top_states = sorted(s for s, _ in Counter(r["state"] for r in rows).most_common(TOP_STATES))
    top_cats = sorted(c for c, _ in Counter(r["category"] for r in rows).most_common(TOP_CATEGORIES))
    dd = [r["delivery_days"] for r in rows]
    fr = [r["freight_ratio"] for r in rows]
    dd_m = sum(dd) / len(dd)
    dd_s = (sum((x - dd_m) ** 2 for x in dd) / len(dd)) ** 0.5 or 1.0
    fr_m = sum(fr) / len(fr)
    fr_s = (sum((x - fr_m) ** 2 for x in fr) / len(fr)) ** 0.5 or 1.0

    names = ["intercept", "late_delivery", "delivery_days_z", "freight_ratio_z"]
    names += [f"state={s}" for s in top_states] + [f"category={c}" for c in top_cats]
    X, y = [], []
    for r in rows:
        row = [1.0, float(r["late"]), (r["delivery_days"] - dd_m) / dd_s,
               (r["freight_ratio"] - fr_m) / fr_s]
        row += [1.0 if r["state"] == s else 0.0 for s in top_states]
        row += [1.0 if r["category"] == c else 0.0 for c in top_cats]
        X.append(row)
        y.append(float(r["satisfied"]))

    k = len(names)
    beta = [0.0] * k
    ridge = 1.0
    last_cov: list[list[float]] = []
    for _ in range(40):
        H = [[0.0] * k for _ in range(k)]
        g = [0.0] * k
        for xi, yi in zip(X, y):
            eta = sum(b * v for b, v in zip(beta, xi))
            p = 1.0 / (1.0 + math.exp(-eta)) if eta >= 0 else math.exp(eta) / (1.0 + math.exp(eta))
            w = max(p * (1 - p), 1e-6)
            resid = yi - p
            for a in range(k):
                g[a] += resid * xi[a]
                for b in range(k):
                    H[a][b] += w * xi[a] * xi[b]
        for a in range(1, k):
            g[a] -= ridge * beta[a]
            H[a][a] += ridge
        cov = _matrix_inverse(H)
        last_cov = cov
        step = [sum(cov[a][b] * g[b] for b in range(k)) for a in range(k)]
        beta = [b + s for b, s in zip(beta, step)]
        if max(abs(s) for s in step) < 1e-8:
            break

    coeffs = []
    for i, nm in enumerate(names):
        se = math.sqrt(last_cov[i][i]) if last_cov[i][i] > 0 else 0.0
        z = beta[i] / se if se > 0 else 0.0
        p = 2.0 * (1.0 - _norm_cdf(abs(z)))
        coeffs.append({"feature": nm, "odds_ratio": round(math.exp(beta[i]), 4),
                        "or_ci_95": [round(math.exp(beta[i] - Z_95 * se), 4),
                                     round(math.exp(beta[i] + Z_95 * se), 4)],
                        "p_value": round(p, 6), "significant": p < 0.05})
    return {"model": "logistic regression, ridge-penalised Newton-Raphson",
            "outcome": "satisfied (review score >= 4)", "n": len(rows),
            "reference": "non-top states/categories pooled as baseline",
            "coefficients": coeffs}


def run(rows: list[dict[str, object]] | None = None) -> dict[str, object]:
    rows = rows if rows is not None else load_reviews()
    total_sat = sum(r["satisfied"] for r in rows)
    lo, hi = wilson_ci(total_sat, len(rows))
    drivers = driver_table(rows)
    return {
        "dataset": "Olist Brazilian E-Commerce (Kaggle, CC BY-NC-SA 4.0) — real",
        "records": len(rows),
        "overall_satisfied_rate": round(total_sat / len(rows), 4),
        "overall_satisfied_ci_95": [lo, hi],
        "nps": nps_summary(rows),
        "drivers": drivers,
        "top_negative_driver": next(
            (d for d in drivers if d["diff_vs_rest"] < 0 and d["significant"]), None),
        "delivery_sla_cohort": delivery_sla_cohort(rows),
        "comment_themes": comment_themes(rows),
        "multivariate_drivers": logistic_drivers(rows),
    }


def _pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def write_reports(result: dict[str, object]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    lo, hi = result["overall_satisfied_ci_95"]
    L = []
    L.append("# CX Driver Analysis (real Olist data)\n")
    L.append(
        f"**{result['records']:,} real reviews** — Olist Brazilian E-Commerce "
        f"(Kaggle, CC BY-NC-SA 4.0), see `data/REAL_DATA_PROVENANCE.md`. "
        f"Overall satisfied rate (score 4-5) **{_pct(result['overall_satisfied_rate'])}** "
        f"(95% CI {_pct(lo)}-{_pct(hi)}, Wilson).\n"
    )

    nps = result["nps"]
    ov = nps["overall"]
    L.append("## Net Promoter Score (disclosed score→band proxy)\n")
    L.append(
        f"NPS proxy: {nps['proxy']}. Overall **NPS {ov['nps']:+.0f}** "
        f"(95% CI [{ov['nps_ci_95'][0]:+.0f}, {ov['nps_ci_95'][1]:+.0f}]) — "
        f"{ov['promoters']:,} promoters, {ov['detractors']:,} detractors of "
        f"{ov['n']:,}.\n"
    )
    L.append("| State | n | NPS | 95% CI |")
    L.append("| --- | ---: | ---: | --- |")
    for s in nps["by_state"]:
        L.append(f"| {s['state']} | {s['n']:,} | {s['nps']:+.0f} | "
                 f"[{s['nps_ci_95'][0]:+.0f}, {s['nps_ci_95'][1]:+.0f}] |")
    L.append("")

    L.append("## Driver ranking (level vs the rest)\n")
    L.append(
        "Two-proportion z-test on the satisfied rate, Cohen's *h*, 95% Wald CI "
        f"on the gap. Only levels with ≥ {MIN_GROUP} reviews; ranked by "
        f"|effect|.\n"
    )
    L.append("| Dimension | Level | n | Satisfied | Δ vs rest | 95% CI (Δ) | Cohen's h | p | Effect |")
    L.append("| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |")
    for d in result["drivers"]:
        flag = "" if d["significant"] else " (n.s.)"
        L.append(
            f"| {d['dimension']} | {d['level']} | {d['n']:,} | "
            f"{_pct(d['satisfied_rate'])} | {d['diff_vs_rest']:+.3f} | "
            f"[{d['diff_ci'][0]:+.3f}, {d['diff_ci'][1]:+.3f}] | "
            f"{d['cohens_h']:+.2f} | {d['p_value']:.4f}{flag} | {d['effect']} |"
        )
    L.append("")
    top = result["top_negative_driver"]
    if top:
        L.append(
            f"**Strongest actionable at-risk cut:** `{top['dimension']} = "
            f"{top['level']}` — satisfied {_pct(top['satisfied_rate'])} vs "
            f"{_pct(top['rest_rate'])} (Δ {top['diff_vs_rest']:+.1%}, "
            f"Cohen's h {top['cohens_h']:+.2f}, {top['effect']}, "
            f"p = {top['p_value']:.4f}).\n"
        )

    coh = result["delivery_sla_cohort"]
    sig = "significant" if coh["significant"] else "not significant"
    L.append("## Delivery-SLA cohort (on-time vs late)\n")
    L.append(
        f"The real lever. On-time deliveries ({coh['on_time_n']:,}) are "
        f"**{_pct(coh['on_time_satisfied_rate'])}** satisfied vs "
        f"**{_pct(coh['late_satisfied_rate'])}** for late ones "
        f"({coh['late_n']:,}) — gap {coh['rate_gap']:+.1%} "
        f"(95% CI [{coh['rate_gap_ci'][0]:+.3f}, {coh['rate_gap_ci'][1]:+.3f}], "
        f"Cohen's h {coh['cohens_h']:+.2f}, {coh['effect']}, "
        f"p = {coh['p_value']:.4f}, {sig}). Mean review score "
        f"{coh['on_time_mean_score']:.2f} on-time vs {coh['late_mean_score']:.2f} "
        f"late. Observational, not a randomised test.\n"
    )

    mv = result["multivariate_drivers"]
    L.append("## Multivariate driver (logistic regression)\n")
    L.append(
        "Each driver's effect on P(satisfied) holding the others constant "
        f"({mv['reference']}); delivery days and freight ratio standardised.\n"
    )
    L.append("| Feature | Odds ratio | 95% CI | p | |")
    L.append("| --- | ---: | --- | ---: | --- |")
    for c in mv["coefficients"]:
        if c["feature"] == "intercept":
            continue
        flag = "" if c["significant"] else " (n.s.)"
        L.append(f"| {c['feature']} | {c['odds_ratio']:.2f} | "
                 f"[{c['or_ci_95'][0]:.2f}, {c['or_ci_95'][1]:.2f}] | "
                 f"{c['p_value']:.4f}{flag} | {'↑' if c['odds_ratio'] > 1 else '↓'} |")
    L.append("")
    lt = next((c for c in mv["coefficients"] if c["feature"] == "late_delivery"), None)
    if lt:
        L.append(
            f"Late delivery is the dominant driver: odds of a satisfied "
            f"review **×{lt['odds_ratio']:.2f}** when an order arrives after "
            f"its estimate, controlling for state, category, delivery time "
            f"and freight (p = {lt['p_value']:.4f}).\n"
        )

    L.append("## Comment themes (Portuguese lexicon, disclosed)\n")
    L.append("| Theme | Mentions | Share of comments | Avg review score |")
    L.append("| --- | ---: | ---: | ---: |")
    for t in result["comment_themes"]:
        L.append(f"| {t['theme']} | {t['mentions']:,} | "
                 f"{_pct(t['share_of_comments'])} | {t['avg_review_score']:.2f} |")
    L.append("")

    L.append("## Boundary\n")
    L.append(
        "Real public e-commerce data (Olist, Kaggle, CC BY-NC-SA 4.0, "
        "non-commercial use, attributed) — no synthetic values. The only "
        "disclosed approximation is the NPS *band* proxy (a relabelling of "
        "the real 1-5 score). Relationships are observational, not causal; "
        "the data is Brazilian marketplace orders 2016-2018 and does not "
        "generalise to other businesses.\n"
    )
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")


def main() -> None:
    result = run()
    write_reports(result)
    print(f"Wrote {METRICS_PATH.relative_to(ROOT)} and {REPORT_PATH.relative_to(ROOT)}")
    top = result["top_negative_driver"]
    if top:
        print(f"Top at-risk driver: {top['dimension']}={top['level']} "
              f"(h={top['cohens_h']:+.2f}, p={top['p_value']:.4f})")


if __name__ == "__main__":
    main()
