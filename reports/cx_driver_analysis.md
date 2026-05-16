# CX Driver Analysis

Sample: **450 synthetic feedback records**. Overall satisfied rate (score 4-5) **47.8%** (95% CI 43.2%-52.4%, Wilson).

## Net Promoter Score

Overall **NPS -36** (95% CI [-44, -29]) — 81 promoters (9-10), 124 passives (7-8), 245 detractors (0-6) of 450. NPS shares the latent driver of CSAT but is a separate construct (see dataset card).

| Segment | n | Promoters | Detractors | NPS | 95% CI |
| --- | ---: | ---: | ---: | ---: | --- |
| First-Time Owners | 120 | 3.3% | 81.7% | -78 | [-87, -70] |
| Performance Enthusiasts | 83 | 18.1% | 53.0% | -35 | [-51, -18] |
| Urban Commuters | 152 | 21.1% | 47.4% | -26 | [-39, -14] |
| Touring Owners | 95 | 31.6% | 32.6% | -1 | [-17, +15] |

Lowest NPS segment: **First-Time Owners** (-78) — the same segment the satisfaction driver analysis flags, so the two lenses agree on where to act.

## Driver ranking (level vs the rest)

Two-proportion z-test on the satisfied rate, Cohen's *h* effect size, 95% Wald CI on the gap. Ranked by |effect|.

| Dimension | Level | n | Satisfied | Δ vs rest | 95% CI (Δ) | Cohen's h | p | Effect |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| friction_score | high (>=4) | 70 | 10.0% | -0.447 | [-0.534, -0.361] | -1.02 | 0.0000 | large |
| segment | First-Time Owners | 120 | 15.0% | -0.447 | [-0.530, -0.364] | -0.97 | 0.0000 | large |
| segment | Touring Owners | 95 | 70.5% | +0.288 | [+0.183, +0.393] | +0.59 | 0.0000 | medium |
| segment | Performance Enthusiasts | 83 | 57.8% | +0.123 | [+0.005, +0.241] | +0.25 | 0.0423 | small |
| journey_stage | Digital | 96 | 57.3% | +0.121 | [+0.009, +0.233] | +0.24 | 0.0354 | small |
| journey_stage | Purchase | 130 | 40.8% | -0.099 | [-0.199, +0.002] | -0.20 | 0.0578 (n.s.) | negligible |
| segment | Urban Commuters | 152 | 53.9% | +0.093 | [-0.004, +0.190] | +0.19 | 0.0613 (n.s.) | negligible |
| region | South | 99 | 41.4% | -0.082 | [-0.192, +0.029] | -0.16 | 0.1512 (n.s.) | negligible |
| region | North | 205 | 52.2% | +0.081 | [-0.011, +0.174] | +0.16 | 0.0862 (n.s.) | negligible |
| journey_stage | Ownership | 99 | 43.4% | -0.056 | [-0.166, +0.055] | -0.11 | 0.3273 (n.s.) | negligible |
| channel | App | 99 | 43.4% | -0.056 | [-0.166, +0.055] | -0.11 | 0.3273 (n.s.) | negligible |
| channel | Dealer | 104 | 51.9% | +0.054 | [-0.056, +0.163] | +0.11 | 0.3345 (n.s.) | negligible |
| journey_stage | Service | 125 | 51.2% | +0.047 | [-0.056, +0.150] | +0.10 | 0.3674 (n.s.) | negligible |
| channel | Email | 98 | 51.0% | +0.042 | [-0.070, +0.153] | +0.08 | 0.4675 (n.s.) | negligible |
| channel | Social | 65 | 44.6% | -0.037 | [-0.168, +0.094] | -0.07 | 0.5811 (n.s.) | negligible |
| region | Central | 146 | 45.9% | -0.028 | [-0.126, +0.070] | -0.06 | 0.5786 (n.s.) | negligible |
| channel | Survey | 84 | 46.4% | -0.017 | [-0.135, +0.102] | -0.03 | 0.7837 (n.s.) | negligible |

**Strongest actionable at-risk cut:** `segment = First-Time Owners` — satisfied rate 15.0% vs 59.7% for the rest (Δ -44.7%, Cohen's h -0.97, large effect, p = 0.0000). This is a population segment operations can target.

_Mechanism (not a targetable cohort): records with friction score >=4 sit at 10.0% satisfied vs 54.7% (Cohen's h -1.02). Friction is near-definitionally tied to satisfaction; it is the lever, the segment cut is where to pull it._

## Multivariate driver (logistic regression)

The bivariate table above does not control for confounding (e.g. a weak segment may just carry more high-friction journeys). This logistic model estimates each driver's effect on P(satisfied) *holding the others constant*. Reference levels: segment=First-Time Owners, journey_stage=Digital, region=Central, channel=App; friction is standardised.

| Feature | Odds ratio | 95% CI | p | |
| --- | ---: | --- | ---: | --- |
| segment=Performance Enthusiasts | 2.58 | [1.30, 5.10] | 0.0067 | ↑ |
| segment=Touring Owners | 4.82 | [2.44, 9.54] | 0.0000 | ↑ |
| segment=Urban Commuters | 2.90 | [1.59, 5.28] | 0.0005 | ↑ |
| journey_stage=Ownership | 0.60 | [0.32, 1.15] | 0.1240 (n.s.) | ↓ |
| journey_stage=Purchase | 0.51 | [0.28, 0.93] | 0.0290 | ↓ |
| journey_stage=Service | 0.60 | [0.33, 1.10] | 0.0976 (n.s.) | ↓ |
| region=North | 1.27 | [0.77, 2.11] | 0.3524 (n.s.) | ↑ |
| region=South | 0.95 | [0.52, 1.72] | 0.8542 (n.s.) | ↓ |
| channel=Dealer | 1.74 | [0.95, 3.21] | 0.0737 (n.s.) | ↑ |
| channel=Email | 1.93 | [1.00, 3.73] | 0.0497 | ↑ |
| channel=Social | 1.71 | [0.83, 3.52] | 0.1431 (n.s.) | ↑ |
| channel=Survey | 1.03 | [0.54, 1.98] | 0.9293 (n.s.) | ↑ |
| friction_score_z | 0.25 | [0.18, 0.34] | 0.0000 | ↓ |

With **First-Time Owners as the reference**, every other segment has a significantly higher odds of being satisfied (OR > 1, all p < 0.05) after controlling for journey stage, region, channel and friction — so the at-risk finding is not a confound. Friction remains the dominant lever (OR 0.25 per +1 SD).

## Follow-up cohort (observational)

Among 244 records needing follow-up, 189 were completed and 55 left open. Post-action satisfied rate is **78.8%** for completed vs **29.1%** for open (gap +49.8%, 95% CI [+0.364, +0.631], Cohen's h +1.05, large effect, p = 0.0000, significant). Mean score change: +1.25 completed vs -0.06 open.

_This is an observational cohort split, not a randomized test: records that get a completed follow-up may differ systematically from those that do not._

## Comment themes

| Theme | Mentions | Share | Avg satisfaction |
| --- | ---: | ---: | ---: |
| Service & parts | 110 | 24.4% | 3.55 |
| Documentation & warranty | 88 | 19.6% | 3.30 |
| Digital onboarding | 81 | 18.0% | 3.52 |
| Financing & pricing | 74 | 16.4% | 3.09 |
| Delivery & handover | 71 | 15.8% | 3.48 |

## Boundary

Data is synthetic with a disclosed generative model (`data/cx_dataset_card.md`); these statistics quantify how cleanly the pipeline recovers an injected structure and are evidence of analytical discipline, not real-world customer truth. All relationships are observational, not causal.
