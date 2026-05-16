# CX Analyst Technical Lab

This lab is the analyst-toolchain layer for the simulated customer-experience case study. It stays inside the CX, Excel, SQL, BI, customer satisfaction, segmentation, trend and insight-brief perimeter.

## What It Shows

- A 450-row feedback sample from a documented deterministic generator
  (`src/generate_cx_dataset.py`, data card in `data/cx_dataset_card.md`).
- Deterministic data validation for required fields, ranges, dates, and follow-up logic.
- Reproducible CX KPI calculation in Python.
- **Statistical driver analysis**: every categorical level vs its complement
  with a two-proportion z-test, Cohen's *h* effect size and 95% CIs, a
  follow-up cohort comparison, and comment-theme extraction
  (`src/cx_driver_analysis.py`).
- SQL views for satisfaction reporting, segment profiling, journey friction, and follow-up tracking.
- Power BI-style star schema and DAX measure catalogue.
- Concise customer satisfaction brief for stakeholder communication.

## Run

From the repository root:

```bash
python cx-analyst-lab/src/generate_cx_dataset.py   # reproduces the sample (seed-fixed)
python cx-analyst-lab/src/validate_cx_data.py
python cx-analyst-lab/src/build_cx_summary.py
python cx-analyst-lab/src/cx_driver_analysis.py    # driver stats + cohort + themes
python -m unittest discover cx-analyst-lab/tests
```

## Boundary

The data is simulated. This is not real customer, dealer, CRM, service, survey or internal process data. The lab is intended to demonstrate Customer Experience analyst discipline, not AI engineering.
