"""Deterministic synthetic CX feedback generator.

This replaces the original 12 hand-typed rows with ~450 rows that follow the
*same* schema and pass the same validator, but are produced from a documented
generative model so the downstream statistics have a real, detectable signal
instead of anecdote.

The model is intentionally transparent (see ``data/cx_dataset_card.md``):
every effect baked into the data is disclosed so the driver analysis is read
as *recovering a known structure*, not discovering truth about real customers.

Pure standard library and a fixed seed: re-running reproduces the byte-identical
CSV, so the committed artifact and CI stay deterministic.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cx_feedback_sample.csv"
CARD_PATH = ROOT / "data" / "cx_dataset_card.md"

SEED = 20260516
N_ROWS = 450
START = date(2026, 1, 6)
END = date(2026, 9, 28)

FIELDS = [
    "feedback_id",
    "date",
    "channel",
    "segment",
    "journey_stage",
    "region",
    "satisfaction_score",
    "feedback_volume",
    "issue_category",
    "friction_score",
    "follow_up_required",
    "follow_up_completed",
    "post_action_score",
    "comment",
]

# --- Documented generative structure (latent "satisfied propensity" in 0..1) ---

SEGMENTS = {
    "Urban Commuters": (0.32, 0.70),
    "Touring Owners": (0.24, 0.74),
    "Performance Enthusiasts": (0.20, 0.72),
    "First-Time Owners": (0.24, 0.50),  # designed at-risk segment
}
JOURNEY_STAGES = {
    "Purchase": (0.28, -0.04),
    "Service": (0.28, -0.02),
    "Digital": (0.22, 0.02),
    "Ownership": (0.22, -0.03),
}
REGIONS = {"North": (0.42, 0.02), "Central": (0.34, 0.0), "South": (0.24, -0.05)}
CHANNELS = {
    "Email": (0.24, 0.0),
    "Dealer": (0.24, 0.02),
    "App": (0.20, 0.0),
    "Survey": (0.18, 0.0),
    "Social": (0.14, -0.03),
}
# First-Time Owners take an extra penalty in financing/documentation moments.
FIRST_TIMER_STAGE_PENALTY = {"Purchase": -0.10, "Ownership": -0.08}

ISSUE_BY_STAGE = {
    "Purchase": ["Financing clarity", "Delivery handover", "Test ride", "Trade-in valuation", "Order tracking"],
    "Service": ["Appointment wait", "Parts availability", "Maintenance clarity", "Repair turnaround", "Service cost transparency"],
    "Digital": ["App onboarding", "Connectivity pairing", "Account access", "Feature discovery", "Digital service booking"],
    "Ownership": ["Documentation", "Insurance documentation", "Warranty registration", "Accessories", "Recall communication"],
}
HARD_ISSUES = {"Financing clarity", "Parts availability", "App onboarding", "Insurance documentation", "Repair turnaround"}

VOLUME_BY_CHANNEL = {
    "Email": (60, 165),
    "Survey": (70, 160),
    "Dealer": (40, 120),
    "App": (35, 130),
    "Social": (28, 90),
}

COMMENT_TEMPLATES = {
    "low": [
        "{issue} was confusing and slowed the whole {stage_l} experience.",
        "Frustrated with {issue_l} during {stage_l}; needed several contacts to resolve.",
        "{issue} created friction and I expected clearer guidance.",
    ],
    "mid": [
        "{issue} was acceptable but {stage_l} could be smoother.",
        "Mixed experience with {issue_l}; resolved eventually after follow-up.",
        "{issue} took longer than expected but the team communicated.",
    ],
    "high": [
        "{issue} was handled smoothly across the {stage_l} journey.",
        "Clear and proactive handling of {issue_l}; very satisfied.",
        "{issue} matched expectations and the {stage_l} step felt effortless.",
    ],
}


def _weighted(rng: random.Random, mapping: dict) -> str:
    keys = list(mapping)
    weights = [mapping[k][0] for k in keys]
    return rng.choices(keys, weights=weights, k=1)[0]


def _clamp_score(value: float) -> int:
    return max(1, min(5, int(round(value))))


def _follow_up_prob(sat: int, friction: int) -> float:
    base = {1: 0.93, 2: 0.90, 3: 0.70, 4: 0.30, 5: 0.12}[sat]
    if friction >= 4:
        base = min(0.97, base + 0.10)
    return base


def generate_rows() -> list[dict[str, str]]:
    rng = random.Random(SEED)
    span_days = (END - START).days
    rows: list[dict[str, str]] = []

    for i in range(1, N_ROWS + 1):
        segment = _weighted(rng, SEGMENTS)
        stage = _weighted(rng, JOURNEY_STAGES)
        region = _weighted(rng, REGIONS)
        channel = _weighted(rng, CHANNELS)

        propensity = SEGMENTS[segment][1]
        propensity += JOURNEY_STAGES[stage][1]
        propensity += REGIONS[region][1]
        propensity += CHANNELS[channel][1]
        if segment == "First-Time Owners":
            propensity += FIRST_TIMER_STAGE_PENALTY.get(stage, 0.0)
        propensity += rng.gauss(0.0, 0.16)
        propensity = max(0.02, min(0.98, propensity))

        satisfaction = _clamp_score(1 + 4 * propensity + rng.gauss(0.0, 0.5))
        friction = _clamp_score(1 + 4 * (1 - propensity) + rng.gauss(0.0, 0.5))

        pool = ISSUE_BY_STAGE[stage]
        if friction >= 4:
            hard = [c for c in pool if c in HARD_ISSUES] or pool
            issue = rng.choice(hard)
        else:
            issue = rng.choice(pool)

        required = rng.random() < _follow_up_prob(satisfaction, friction)
        if required:
            completed = rng.random() < 0.78
        else:
            completed = False

        if completed:
            uplift = rng.choices([1, 2], weights=[0.62, 0.38], k=1)[0]
            post = _clamp_score(satisfaction + uplift + rng.gauss(0.0, 0.4))
        elif required:
            post = _clamp_score(satisfaction + rng.gauss(-0.1, 0.3))
        else:
            post = satisfaction

        lo, hi = VOLUME_BY_CHANNEL[channel]
        volume = rng.randint(lo, hi)

        bucket = "low" if satisfaction <= 2 else "mid" if satisfaction == 3 else "high"
        template = rng.choice(COMMENT_TEMPLATES[bucket])
        comment = template.format(
            issue=issue,
            issue_l=issue.lower(),
            stage_l=stage.lower(),
        )

        day = rng.randint(0, span_days)
        rows.append(
            {
                "feedback_id": f"FB-{i:04d}",
                "date": (START + timedelta(days=day)).isoformat(),
                "channel": channel,
                "segment": segment,
                "journey_stage": stage,
                "region": region,
                "satisfaction_score": str(satisfaction),
                "feedback_volume": str(volume),
                "issue_category": issue,
                "friction_score": str(friction),
                "follow_up_required": "yes" if required else "no",
                "follow_up_completed": "yes" if completed else "no",
                "post_action_score": str(post),
                "comment": comment,
            }
        )

    rows.sort(key=lambda r: (r["date"], r["feedback_id"]))
    return rows


def write_dataset(rows: list[dict[str, str]]) -> None:
    with DATA_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_card(rows: list[dict[str, str]]) -> None:
    n = len(rows)
    months = sorted({r["date"][:7] for r in rows})
    card = f"""# CX Feedback Dataset Card

## Summary

- **File:** `data/cx_feedback_sample.csv`
- **Rows:** {n} synthetic feedback records
- **Period:** {months[0]} to {months[-1]} ({len(months)} months)
- **Generator:** `src/generate_cx_dataset.py`, seed `{SEED}` (re-running reproduces the file byte-for-byte)
- **Status:** SYNTHETIC. Not real customer, dealer, CRM, survey, warranty or service data.

## Why this exists

The original sample was 12 hand-typed rows, which is too thin for any honest
proportion test, effect size or cohort comparison. This generator produces a
larger sample in the **identical schema and validator**, built from an openly
documented model so the driver analysis is read as *recovering a known
structure* — not as a discovery about real people.

## Disclosed generative structure

The latent quantity is a "satisfied propensity" in 0..1 mapped to the 1-5
`satisfaction_score` (and inversely to `friction_score`, which is why the two
are strongly negatively correlated by construction).

| Factor | Effect on propensity |
| --- | --- |
| Segment baseline | First-Time Owners 0.50 (at-risk); others 0.70-0.74 |
| First-Time Owners × Purchase / Ownership | extra -0.10 / -0.08 (financing & documentation) |
| Journey stage | Purchase -0.04, Service -0.02, Digital +0.02, Ownership -0.03 |
| Region | North +0.02, Central 0.00, South -0.05 |
| Channel | Dealer +0.02, Social -0.03, others ~0 |
| Noise | Gaussian, sd 0.16 |

`follow_up_required` rises as satisfaction falls / friction rises; ~78% of
required follow-ups are completed (an operational backlog is left on purpose).
A completed follow-up adds a +1/+2 uplift to `post_action_score`; an
uncompleted-but-required one does not — this is the intended intervention
signal the cohort analysis recovers.

## Boundary

All effects above are *injected*. The statistics in
`reports/cx_driver_analysis.md` quantify how cleanly an analyst pipeline
recovers them; they are evidence of analytical discipline, not real-world
customer truth, and the relationships are observational, not causal.
"""
    CARD_PATH.write_text(card, encoding="utf-8")


def main() -> None:
    rows = generate_rows()
    write_dataset(rows)
    write_card(rows)
    print(f"Wrote {len(rows)} rows to {DATA_PATH.relative_to(ROOT)}")
    print(f"Wrote dataset card to {CARD_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
