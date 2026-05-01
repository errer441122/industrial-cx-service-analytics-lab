# CX Analyst Technical Lab

This lab is the analyst-toolchain layer for the Ducati Customer Experience case study. It stays inside the CX, Excel, SQL, BI, customer satisfaction, segmentation, trend, and insight-brief perimeter.

## What It Shows

- Customer feedback data organized in a reporting-ready CSV.
- Deterministic data validation for required fields, ranges, dates, and follow-up logic.
- Reproducible CX KPI calculation in Python.
- SQL views for satisfaction reporting, segment profiling, journey friction, and follow-up tracking.
- Power BI-style star schema and DAX measure catalogue.
- Concise customer satisfaction brief for stakeholder communication.

## Run

From the repository root:

```bash
python cx-analyst-lab/src/validate_cx_data.py
python cx-analyst-lab/src/build_cx_summary.py
python -m unittest discover cx-analyst-lab/tests
```

## Boundary

The data is simulated. This is not Ducati customer, dealer, CRM, service, survey, or internal process data. The lab is intended to demonstrate Customer Experience analyst discipline, not AI engineering.
