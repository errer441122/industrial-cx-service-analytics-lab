# CX & Service Analytics Lab

A reviewable customer-experience analytics case study on the **real**
public *Olist Brazilian E-Commerce* dataset (Kaggle, CC BY-NC-SA 4.0). A
hiring manager can open one repo, read a decision-style analysis, and check
the code and tests behind every number. Positioned for **Customer
Experience / Customer Insights / CX Analyst** internships.

## What it shows

- **Real data, disclosed provenance.** `src/prepare_real_data.py` joins the
  Olist reviews/orders/customers/items/products into
  `data/olist_reviews.csv` (~95k real reviews) + `olist_review_comments.csv`
  (Portuguese review text). Source, license, cleaning rules and SHA256 are
  in `data/REAL_DATA_PROVENANCE.md`. CI re-verifies the checksum.
- **Statistical driver analysis**: every categorical level (state,
  category, delivery speed, freight level, late delivery) vs its complement
  with a two-proportion z-test, Cohen's *h* and a 95% CI, ranked by effect,
  with a small-n floor (`src/cx_driver_analysis.py`).
- **Net Promoter Score** from a *disclosed* score→band proxy (5=promoter,
  4=passive, ≤3=detractor — Olist has no 0-10 question): overall NPS with a
  variance-based 95% CI and NPS by state.
- **Delivery-SLA cohort**: on-time vs late delivery effect on satisfaction
  (the real, dominant lever) with effect size and mean-score gap.
- **Multivariate logistic regression** for P(satisfied): each driver's odds
  ratio *controlling for the others* (state, category, delivery time,
  freight, late delivery).
- **Comment themes** from a disclosed Portuguese keyword lexicon over the
  real review text.
- A stakeholder satisfaction brief (`reports/customer_satisfaction_brief.md`).

## Recruiter 5-minute route

1. `reports/cx_driver_analysis.md` — NPS, driver ranking, delivery-SLA
   cohort, multivariate model and comment themes.
2. `reports/customer_satisfaction_brief.md` — the stakeholder summary.
3. `data/REAL_DATA_PROVENANCE.md` — source, license (CC BY-NC-SA 4.0),
   cleaning rules and checksums.

## Run

Olist requires a Kaggle login, so the source is not auto-downloaded:
download `olistbr/brazilian-ecommerce` and save it as `.cache/olist.zip`
(git-ignored), then from the repository root:

```bash
python src/prepare_real_data.py      # joins Olist -> data/olist_reviews.csv (+ provenance)
python src/validate_cx_data.py
python src/build_cx_summary.py
python src/cx_driver_analysis.py      # NPS + drivers + SLA cohort + multivariate
python -m unittest discover -s tests
```

Pure Python standard library — no third-party dependencies. The prepared
CSVs are committed, so the analysis and tests run without the source.

## Repository structure

| Path | Purpose |
| --- | --- |
| `src/prepare_real_data.py` | Joins the Olist source into the committable real CSVs + provenance. |
| `src/validate_cx_data.py` | Schema/range/consistency validation of the real extract. |
| `src/cx_driver_analysis.py` | Driver ranking, NPS, delivery-SLA cohort, multivariate logistic, themes. |
| `src/build_cx_summary.py` | Stakeholder KPI brief and monthly trend. |
| `data/` | Real prepared reviews + comments + `REAL_DATA_PROVENANCE.md`. |
| `reports/` | Driver analysis, metrics JSON and the satisfaction brief. |
| `tests/` | Behavioral tests: methodological correctness on the real data. |

## Boundary

Real public e-commerce data — Olist Brazilian E-Commerce (Kaggle,
**CC BY-NC-SA 4.0**, used non-commercially for a job-application portfolio,
attributed). No synthetic values. The only disclosed approximation is the
NPS *band* proxy (a relabelling of the real 1-5 review score, not invented
data). Relationships are observational, not causal; the data is Brazilian
marketplace orders 2016-2018 and does not generalise to other businesses.
