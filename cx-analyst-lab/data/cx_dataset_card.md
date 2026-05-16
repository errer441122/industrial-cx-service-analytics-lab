# CX Feedback Dataset Card

## Summary

- **File:** `data/cx_feedback_sample.csv`
- **Rows:** 450 synthetic feedback records
- **Period:** 2026-01 to 2026-09 (9 months)
- **Generator:** `src/generate_cx_dataset.py`, seed `20260516` (re-running reproduces the file byte-for-byte)
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
