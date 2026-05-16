# CX & Service Analytics Lab

A reviewable customer-experience analytics case study on a **disclosed
synthetic** dataset. A hiring manager can open one repo, read a
decision-style analysis, and check the code and tests behind every number.
Positioned for **Customer Experience / Customer Insights / CX Analyst**
internships.

## What it shows

- A 450-row feedback sample from a documented deterministic generator
  (`src/generate_cx_dataset.py`, data card in `data/cx_dataset_card.md`) —
  no hand-tuned numbers, byte-stable, re-validated in CI.
- Deterministic data validation for required fields, ranges, dates and
  follow-up logic (`src/validate_cx_data.py`).
- **Statistical driver analysis**: every categorical level vs its
  complement with a two-proportion z-test, Cohen's *h* effect size and 95%
  CIs, a follow-up cohort comparison, and comment-theme extraction
  (`src/cx_driver_analysis.py`).
- **Net Promoter Score**: promoter/passive/detractor banding, overall NPS
  with a variance-based 95% CI, and NPS by segment as a second lens that
  agrees with the at-risk segment CSAT flags.
- **Multivariate logistic regression** for P(satisfied): each driver's odds
  ratio *controlling for the others*, so a bivariate finding is shown to
  survive (or not) confounding by journey stage, region and friction.
- SQL reporting views, a Power BI star schema + DAX measure catalogue, and
  a stakeholder satisfaction brief.

## Recruiter 5-minute route

1. `reports/cx_driver_analysis.md` — NPS, driver ranking, multivariate
   model, follow-up cohort and comment themes.
2. `reports/customer_satisfaction_brief.md` — the stakeholder summary.
3. `data/cx_dataset_card.md` — exactly what is simulated and how.
4. `sql/cx_reporting_views.sql` and `powerbi/` — BI-side evidence.
5. `dashboard-workbook/customer_experience_dashboard.xlsx` — the workbook.

## Run

From the repository root:

```bash
python src/generate_cx_dataset.py   # reproduces the sample (seed-fixed)
python src/validate_cx_data.py
python src/build_cx_summary.py
python src/cx_driver_analysis.py     # NPS + drivers + multivariate + cohort
python -m unittest discover -s tests
```

Pure Python standard library — no third-party dependencies.

## Repository structure

| Path | Purpose |
| --- | --- |
| `src/` | Generator, validator, KPI summary and the statistical driver/NPS/logistic analysis. |
| `data/` | Synthetic feedback sample and its data card. |
| `reports/` | Driver analysis, metrics JSON and the stakeholder satisfaction brief. |
| `sql/` | CX reporting views. |
| `powerbi/` | Star schema and DAX measure catalogue. |
| `dashboard-workbook/` | Excel CX dashboard workbook. |
| `tests/` | Behavioral tests asserting recovered structure, not frozen snapshots. |

## Boundary

The data is simulated with a disclosed generative model. This is not real
customer, dealer, CRM, service or survey data. The statistics quantify how
cleanly the pipeline recovers an injected structure — evidence of analytical
discipline, not real-world customer truth — and all relationships are
observational, not causal.
