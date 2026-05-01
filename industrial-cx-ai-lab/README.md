# Industrial CX AI Lab

This lab upgrades the Ducati CX workbook from dashboard-only evidence to a small AI/data-engineering project. It uses simulated after-sales and telemetry-style data to connect customer experience, service operations, Industrial IoT, anomaly detection, and service-risk scoring.

It uses simulated data only. It does not represent Ducati systems, customers, dealers, motorcycles, telemetry, or internal processes.

## What It Demonstrates

- Deterministic simulated time-series telemetry with controlled anomaly injection.
- Expected fields: `timestamp`, `asset_id`, `rpm`, `temperature_c`, `vibration_mm_s`, `pressure_bar`, `torque_nm`, `operating_hours`, `error_code_count`, `service_delay_days`, `customer_satisfaction_score`, `anomaly_label`, and `service_escalation_label`.
- Rule-based anomaly baseline and IsolationForest anomaly benchmark.
- Service-risk classifier with ROC-AUC, PR-AUC, F1, precision, recall, and feature importance.
- Influx line protocol export for time-series monitoring review.
- Simulated OPC UA, MQTT, Influx, Grafana, and Telegraf design artifacts in `ops/`.
- Maintenance policy note with human-in-the-loop boundaries.
- Slurm batch packaging for HPC-style scoring.

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
python industrial-cx-ai-lab/src/run_pipeline.py
python -m pytest -q industrial-cx-ai-lab/tests
```

Outputs are written to `industrial-cx-ai-lab/artifacts/` and ignored by git.

Key outputs:

- `artifacts/anomaly_metrics.json`
- `artifacts/service_risk_metrics.json`
- `artifacts/feature_importance.csv`
- `artifacts/maintenance_policy_note.md`
- `artifacts/influx_line_protocol.txt`

## Reviewer Boundary

The classifier is advisory. It flags records for human service review; it does not automate a customer decision, warranty decision, or commercial action.
