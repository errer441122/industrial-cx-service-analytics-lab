# PwC Analytics Story

This repository is useful for PwC-style Data & AI consulting review because it translates messy operational signals into a clear business workflow: measure customer friction, segment the issue, prioritize action, and communicate what the model can and cannot decide.

## Client-Style Narrative

The CX workbook shows the front-office layer: customer satisfaction, journey bottlenecks, segment prioritization, and action tracking. The industrial lab adds a technical supplement: simulated telemetry, anomaly detection, service-risk scoring, and reviewer-readable metrics.

## What A PwC Reviewer Can Inspect

| Consulting signal | Evidence |
| --- | --- |
| Data-to-insight storytelling | `index.html`, `dashboard-workbook/customer_experience_dashboard.xlsx` |
| KPI and segmentation logic | `cx-data.js`, `cx-analyst-lab/` |
| SQL / analytics engineering | `sql/reviewer_service_mart.duckdb.sql` |
| ML communication | `industrial-cx-ai-lab/artifacts/maintenance_policy_note.md` |
| Model limits | `docs/reviewer/CLAIMS_AND_LIMITATIONS.md` |

## Recommended Framing

> I used a CX workbook as the business communication layer, then added a simulated industrial analytics lab so the same service-friction story can be reviewed from a technical angle: telemetry, anomaly features, service-risk scoring, monitoring artifacts, and human review.

Do not frame this as a real Ducati client project or a production AI deployment.
