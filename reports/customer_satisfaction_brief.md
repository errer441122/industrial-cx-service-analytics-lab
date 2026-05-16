# Customer Satisfaction Brief

## Executive Readout

Across **450 feedback records** (41,018 weighted feedback-volume units), the
weighted customer satisfaction rate is **54.0%** and the score-level satisfied
rate is **53.1%** (95% CI 48.5%–57.7%, Wilson). The headline is not the
average — it is the **gap between segments**: First-Time Owners sit at a
**14.8% satisfied rate vs 64.2% for everyone else** (Δ −49 pts, Cohen's
h −1.07, large effect, p < 0.0001). They are the only at-risk segment and the
single highest-leverage place to act.

## KPI Snapshot

| Metric | Value | Analyst note |
| --- | ---: | --- |
| Customer Satisfaction Rate | 54.0% | Weighted share of feedback volume with satisfaction score 4–5 |
| Satisfied Rate (record-level) | 53.1% | 95% CI 48.5%–57.7% (Wilson) |
| Weighted Feedback Volume | 41,018 | Sum of feedback-volume units |
| At-Risk Segment Count | 1 | First-Time Owners below the satisfaction/friction threshold |
| Journey Friction Index | 2.48 / 5 | Weighted friction score across all journey stages |
| Follow-up Completion Rate | 76.1% | 175 of 230 required follow-ups completed |
| Post-Action Improvement Delta | +1.21 | Mean score lift after completed follow-ups |

## What Drives the Gap

Every categorical level was tested against its complement with a
two-proportion z-test, Cohen's *h* and a 95% CI (full table in
[`cx_driver_analysis.md`](cx_driver_analysis.md)):

- **First-Time Owners** — satisfied rate 14.8% vs 64.2% rest; large negative
  effect (h −1.07, p < 0.0001). Segment avg satisfaction **2.76 / 5** and avg
  friction **3.32 / 5**, both worst of the four segments.
- **Friction is the mechanism, not a cohort.** Records with friction ≥ 4 sit
  at 2.9% satisfied vs 62.2% — near-definitional, so it is reported as the
  lever, while the *segment* cut is where to pull it.
- Touring Owners (+19 pts) and Urban Commuters (+18 pts) are significantly
  *above* the rest; Performance Enthusiasts and all region splits are not
  statistically distinguishable.

## Does Follow-up Work?

Among the 230 records that required follow-up, the post-action satisfied rate
is **80.0% for completed vs 29.1% for open** (gap +50.9 pts, 95% CI
+37.5 to +64.3, Cohen's h +1.08, p < 0.0001). Mean score change is
**+1.21 for completed vs −0.04 for open**. This is an *observational* cohort
split, not a randomized test — completed and open records may differ
systematically — but the size and consistency of the gap make closing the
55 open follow-ups the clearest operational win.

## Comment Themes

| Theme | Mentions | Avg satisfaction |
| --- | ---: | ---: |
| Service & parts | 110 | 3.45 |
| Digital onboarding | 98 | 3.78 |
| Financing & pricing | 91 | **3.15** |
| Documentation & warranty | 69 | 3.45 |
| Delivery & handover | 58 | 4.00 |

Financing & pricing carries the lowest comment-level satisfaction — coherent
with the First-Time Owner pain in purchase and ownership moments.

## Recommended Actions

1. Treat **First-Time Owners** as a tracked cohort: financing-comparison
   templates and documentation walkthroughs at purchase and ownership.
2. Clear the **55 open required follow-ups**; the cohort gap quantifies the
   expected satisfaction recovery.
3. Add dealer callback triggers when friction score ≥ 4 (the dominant lever).
4. Put **Financing & pricing** comment volume on the weekly CX dashboard as a
   leading indicator for the First-Time Owner segment.

## Stakeholder Handoff

CX owns the insight brief, dealers own callback completion, digital owns
onboarding clarity, CRM owns follow-up tracking. Next dashboard check:
First-Time Owner satisfied rate and the open-follow-up count after the
documentation fix.

## Boundary

Data is synthetic with a fully disclosed generative model
(`data/cx_dataset_card.md`); the statistics quantify how cleanly an analyst
pipeline recovers an injected structure and are evidence of analytical
discipline, not real-world customer truth. All relationships are
observational, not causal.
