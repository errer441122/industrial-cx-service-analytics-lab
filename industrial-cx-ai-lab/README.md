# Industrial CX AI Lab

This lab upgrades the Ducati CX workbook from dashboard-only evidence to a small AI/data-engineering project. It uses simulated after-sales and telemetry-style data to connect customer experience, service operations, Industrial IoT, and risk scoring.

It uses simulated data only. It does not represent Ducati systems, customers, dealers, motorcycles, telemetry, or internal processes.

## What It Demonstrates

- OPC UA/Kepware-style tag naming for simulated field data.
- Industrial after-sales telemetry features: vibration, temperature, oil pressure, battery voltage, service delay, warranty claims, and telemetry dropouts.
- Text-mining features from customer notes.
- Anomaly feature engineering for service-risk triage.
- A reproducible ML classifier for churn/service escalation risk.
- SQLite feature mart for SQL/data-engineering review.
- Influx line protocol export for time-series monitoring.
- Grafana dashboard JSON stub for BI-REX/industrial monitoring relevance.
- Slurm batch script for HPC-style scoring.

## Why This Exists

The original workbook was useful for analytics and stakeholder communication but too weak for AI engineering. This folder adds technical evidence for PwC Data & AI, BI-REX AI/Industrial IoT, and CINECA/IT4LIA-style workload packaging.

| Internship signal | Evidence in this lab |
| --- | --- |
| PwC Data & AI | ML classifier, feature mart, model card, reproducible metrics |
| BI-REX | OPC UA-style data, time-series export, Grafana stub, industrial anomaly signals |
| CINECA / IT4LIA | Slurm-ready batch script and packaged AI workload |
| CRIF | Text features, risk triage, transparent model limitations |
| UNDP | Responsible AI boundary and human escalation framing |

## Run Locally

From the repository root:

```bash
python3 industrial-cx-ai-lab/src/run_pipeline.py
python3 -m unittest discover industrial-cx-ai-lab/tests
```

Outputs are written to `industrial-cx-ai-lab/artifacts/` and ignored by git.

## Reviewer Boundary

The classifier is advisory. It flags records for human service review; it does not automate a customer decision, warranty decision, or commercial action.
