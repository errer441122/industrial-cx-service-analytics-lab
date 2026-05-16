# CX Driver Analysis

Sample: **450 synthetic feedback records**. Overall satisfied rate (score 4-5) **53.1%** (95% CI 48.5%-57.7%, Wilson).

## Driver ranking (level vs the rest)

Two-proportion z-test on the satisfied rate, Cohen's *h* effect size, 95% Wald CI on the gap. Ranked by |effect|.

| Dimension | Level | n | Satisfied | Δ vs rest | 95% CI (Δ) | Cohen's h | p | Effect |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| friction_score | high (>=4) | 69 | 2.9% | -0.593 | [-0.656, -0.530] | -1.48 | 0.0000 | large |
| segment | First-Time Owners | 101 | 14.8% | -0.493 | [-0.579, -0.408] | -1.07 | 0.0000 | large |
| segment | Touring Owners | 105 | 67.6% | +0.189 | [+0.085, +0.293] | +0.39 | 0.0007 | small |
| segment | Urban Commuters | 141 | 65.2% | +0.177 | [+0.080, +0.273] | +0.36 | 0.0005 | small |
| journey_stage | Digital | 108 | 63.9% | +0.142 | [+0.037, +0.247] | +0.29 | 0.0100 | small |
| channel | Email | 114 | 62.3% | +0.123 | [+0.019, +0.227] | +0.25 | 0.0232 | small |
| journey_stage | Service | 139 | 45.3% | -0.113 | [-0.212, -0.013] | -0.23 | 0.0269 | small |
| channel | App | 90 | 45.6% | -0.094 | [-0.209, +0.021] | -0.19 | 0.1083 (n.s.) | negligible |
| channel | Social | 65 | 46.2% | -0.081 | [-0.212, +0.050] | -0.16 | 0.2243 (n.s.) | negligible |
| segment | Performance Enthusiasts | 103 | 59.2% | +0.079 | [-0.029, +0.188] | +0.16 | 0.1569 (n.s.) | negligible |
| region | North | 188 | 55.9% | +0.047 | [-0.046, +0.140] | +0.09 | 0.3238 (n.s.) | negligible |
| region | Central | 164 | 50.6% | -0.039 | [-0.135, +0.057] | -0.08 | 0.4207 (n.s.) | negligible |
| journey_stage | Purchase | 120 | 51.7% | -0.020 | [-0.124, +0.085] | -0.04 | 0.7112 (n.s.) | negligible |
| journey_stage | Ownership | 83 | 54.2% | +0.014 | [-0.105, +0.132] | +0.03 | 0.8231 (n.s.) | negligible |
| region | South | 98 | 52.0% | -0.014 | [-0.126, +0.098] | -0.03 | 0.8103 (n.s.) | negligible |
| channel | Survey | 82 | 53.7% | +0.007 | [-0.113, +0.126] | +0.01 | 0.9125 (n.s.) | negligible |
| channel | Dealer | 99 | 53.5% | +0.005 | [-0.106, +0.117] | +0.01 | 0.9237 (n.s.) | negligible |

**Strongest actionable at-risk cut:** `segment = First-Time Owners` — satisfied rate 14.8% vs 64.2% for the rest (Δ -49.3%, Cohen's h -1.07, large effect, p = 0.0000). This is a population segment operations can target.

_Mechanism (not a targetable cohort): records with friction score >=4 sit at 2.9% satisfied vs 62.2% (Cohen's h -1.48). Friction is near-definitionally tied to satisfaction; it is the lever, the segment cut is where to pull it._

## Follow-up cohort (observational)

Among 230 records needing follow-up, 175 were completed and 55 left open. Post-action satisfied rate is **80.0%** for completed vs **29.1%** for open (gap +50.9%, 95% CI [+0.375, +0.643], Cohen's h +1.07, large effect, p = 0.0000, significant). Mean score change: +1.21 completed vs -0.04 open.

_This is an observational cohort split, not a randomized test: records that get a completed follow-up may differ systematically from those that do not._

## Comment themes

| Theme | Mentions | Share | Avg satisfaction |
| --- | ---: | ---: | ---: |
| Service & parts | 110 | 24.4% | 3.45 |
| Digital onboarding | 98 | 21.8% | 3.78 |
| Financing & pricing | 91 | 20.2% | 3.15 |
| Documentation & warranty | 69 | 15.3% | 3.45 |
| Delivery & handover | 58 | 12.9% | 4.00 |

## Boundary

Data is synthetic with a disclosed generative model (`data/cx_dataset_card.md`); these statistics quantify how cleanly the pipeline recovers an injected structure and are evidence of analytical discipline, not real-world customer truth. All relationships are observational, not causal.
