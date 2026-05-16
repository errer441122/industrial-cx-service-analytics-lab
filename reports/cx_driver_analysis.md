# CX Driver Analysis (real Olist data)

**95,639 real reviews** — Olist Brazilian E-Commerce (Kaggle, CC BY-NC-SA 4.0), see `data/REAL_DATA_PROVENANCE.md`. Overall satisfied rate (score 4-5) **79.0%** (95% CI 78.7%-79.2%, Wilson).

## Net Promoter Score (disclosed score→band proxy)

NPS proxy: score 5=promoter, 4=passive, ≤3=detractor. Overall **NPS +38** (95% CI [+38, +39]) — 56,667 promoters, 20,110 detractors of 95,639.

| State | n | NPS | 95% CI |
| --- | ---: | ---: | --- |
| MA | 709 | +19 | [+12, +25] |
| BA | 3,222 | +23 | [+20, +26] |
| PA | 928 | +24 | [+18, +29] |
| CE | 1,273 | +25 | [+20, +30] |
| PI | 470 | +28 | [+21, +36] |
| RJ | 12,180 | +30 | [+28, +31] |
| ES | 1,970 | +33 | [+29, +36] |
| PB | 511 | +33 | [+26, +40] |
| GO | 1,944 | +33 | [+30, +37] |
| PE | 1,580 | +35 | [+31, +39] |
| SC | 3,512 | +36 | [+34, +39] |
| MT | 877 | +37 | [+31, +42] |
| DF | 2,065 | +37 | [+33, +40] |
| RN | 470 | +38 | [+30, +45] |
| MS | 699 | +39 | [+33, +45] |
| RS | 5,319 | +40 | [+37, +42] |
| MG | 11,265 | +40 | [+39, +42] |
| PR | 4,887 | +43 | [+41, +45] |
| SP | 40,190 | +43 | [+42, +44] |

## Driver ranking (level vs the rest)

Two-proportion z-test on the satisfied rate, Cohen's *h*, 95% Wald CI on the gap. Only levels with ≥ 400 reviews; ranked by |effect|.

| Dimension | Level | n | Satisfied | Δ vs rest | 95% CI (Δ) | Cohen's h | p | Effect |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| late_delivery | late (delivered after estimate) | 6,362 | 26.7% | -0.560 | [-0.571, -0.549] | -1.20 | 0.0000 | large |
| delivery_speed | slow (15d+) | 26,024 | 64.6% | -0.197 | [-0.203, -0.191] | -0.46 | 0.0000 | small |
| delivery_speed | fast (≤7d) | 33,500 | 86.0% | +0.107 | [+0.102, +0.113] | +0.27 | 0.0000 | small |
| delivery_speed | normal (8-14d) | 36,115 | 82.8% | +0.062 | [+0.057, +0.067] | +0.15 | 0.0000 | negligible |
| customer_state | RJ | 12,180 | 73.5% | -0.063 | [-0.071, -0.055] | -0.15 | 0.0000 | negligible |
| product_category | bed_bath_table | 9,040 | 74.4% | -0.050 | [-0.059, -0.041] | -0.12 | 0.0000 | negligible |
| customer_state | SP | 40,190 | 81.5% | +0.043 | [+0.037, +0.048] | +0.10 | 0.0000 | negligible |
| product_category | telephony | 4,048 | 76.0% | -0.031 | [-0.045, -0.018] | -0.07 | 0.0000 | negligible |
| customer_state | PR | 4,887 | 81.6% | +0.028 | [+0.017, +0.039] | +0.07 | 0.0000 | negligible |
| product_category | sports_leisure | 7,426 | 81.5% | +0.028 | [+0.018, +0.037] | +0.07 | 0.0000 | negligible |
| product_category | furniture_decor | 6,143 | 76.4% | -0.028 | [-0.039, -0.017] | -0.07 | 0.0000 | negligible |
| product_category | health_beauty | 8,548 | 81.0% | +0.023 | [+0.014, +0.032] | +0.06 | 0.0000 | negligible |
| freight_level | high freight | 36,871 | 77.7% | -0.021 | [-0.026, -0.016] | -0.05 | 0.0000 | negligible |
| freight_level | low freight | 25,139 | 80.4% | +0.019 | [+0.013, +0.025] | +0.05 | 0.0000 | negligible |
| product_category | computers_accessories | 6,449 | 77.5% | -0.016 | [-0.027, -0.006] | -0.04 | 0.0022 | negligible |
| product_category | watches_gifts | 5,429 | 77.9% | -0.012 | [-0.023, -0.000] | -0.03 | 0.0382 | negligible |
| customer_state | MG | 11,265 | 80.0% | +0.011 | [+0.003, +0.019] | +0.03 | 0.0060 | negligible |
| product_category | housewares | 5,652 | 80.0% | +0.011 | [+0.000, +0.022] | +0.03 | 0.0492 | negligible |
| customer_state | RS | 5,319 | 79.9% | +0.009 | [-0.002, +0.021] | +0.02 | 0.1006 (n.s.) | negligible |
| customer_state | SC | 3,512 | 78.2% | -0.008 | [-0.022, +0.005] | -0.02 | 0.2287 (n.s.) | negligible |
| freight_level | mid freight | 33,629 | 79.4% | +0.006 | [+0.001, +0.011] | +0.01 | 0.0293 | negligible |

**Strongest actionable at-risk cut:** `late_delivery = late (delivered after estimate)` — satisfied 26.7% vs 82.7% (Δ -56.0%, Cohen's h -1.20, large, p = 0.0000).

## Delivery-SLA cohort (on-time vs late)

The real lever. On-time deliveries (89,277) are **82.7%** satisfied vs **26.7%** for late ones (6,362) — gap +56.0% (95% CI [+0.549, +0.571], Cohen's h +1.20, large, p = 0.0000, significant). Mean review score 4.29 on-time vs 2.27 late. Observational, not a randomised test.

## Multivariate driver (logistic regression)

Each driver's effect on P(satisfied) holding the others constant (non-top states/categories pooled as baseline); delivery days and freight ratio standardised.

| Feature | Odds ratio | 95% CI | p | |
| --- | ---: | --- | ---: | --- |
| late_delivery | 0.18 | [0.17, 0.20] | 0.0000 | ↓ |
| delivery_days_z | 0.65 | [0.63, 0.67] | 0.0000 | ↓ |
| freight_ratio_z | 0.95 | [0.94, 0.97] | 0.0000 | ↓ |
| state=MG | 0.85 | [0.79, 0.90] | 0.0000 | ↓ |
| state=PR | 0.94 | [0.86, 1.02] | 0.1464 (n.s.) | ↓ |
| state=RJ | 0.79 | [0.74, 0.84] | 0.0000 | ↓ |
| state=RS | 1.04 | [0.96, 1.13] | 0.3609 (n.s.) | ↑ |
| state=SC | 0.95 | [0.86, 1.04] | 0.2893 (n.s.) | ↓ |
| state=SP | 0.79 | [0.75, 0.84] | 0.0000 | ↓ |
| category=bed_bath_table | 0.74 | [0.70, 0.78] | 0.0000 | ↓ |
| category=computers_accessories | 0.86 | [0.81, 0.92] | 0.0000 | ↓ |
| category=furniture_decor | 0.82 | [0.77, 0.88] | 0.0000 | ↓ |
| category=health_beauty | 1.08 | [1.02, 1.16] | 0.0132 | ↑ |
| category=housewares | 0.93 | [0.86, 1.00] | 0.0537 (n.s.) | ↓ |
| category=sports_leisure | 1.11 | [1.04, 1.19] | 0.0028 | ↑ |
| category=telephony | 0.81 | [0.74, 0.88] | 0.0000 | ↓ |
| category=watches_gifts | 0.86 | [0.80, 0.93] | 0.0001 | ↓ |

Late delivery is the dominant driver: odds of a satisfied review **×0.18** when an order arrives after its estimate, controlling for state, category, delivery time and freight (p = 0.0000).

## Comment themes (Portuguese lexicon, disclosed)

| Theme | Mentions | Share of comments | Avg review score |
| --- | ---: | ---: | ---: |
| Produto & qualidade | 17,822 | 45.9% | 3.59 |
| Entrega & prazo | 15,536 | 40.0% | 4.03 |
| Recomendação / satisfação | 10,762 | 27.7% | 4.52 |
| Não recebido / faltou | 2,598 | 6.7% | 1.62 |
| Atendimento | 2,011 | 5.2% | 2.69 |

## Boundary

Real public e-commerce data (Olist, Kaggle, CC BY-NC-SA 4.0, non-commercial use, attributed) — no synthetic values. The only disclosed approximation is the NPS *band* proxy (a relabelling of the real 1-5 score). Relationships are observational, not causal; the data is Brazilian marketplace orders 2016-2018 and does not generalise to other businesses.
