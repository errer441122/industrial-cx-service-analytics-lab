# Evidence Map - Ducati Customer Experience Data Analyst

This file maps the Customer Experience Data Analyst requirements and AI/data internship signals to concrete project evidence.

| Requirement | Where to inspect it | Evidence shown |
| --- | --- | --- |
| Collect, organize, and analyze customer data | `index.html`, `cx-data.js`, `dashboard-workbook/customer_experience_dashboard.xlsx` | Simulated survey/CRM/service/dealer/digital-touchpoint data model and dashboard workflow |
| Customer satisfaction reporting | Live workbook `Reporting` section, Excel `Dashboard` sheet, `cx-analyst-lab/reports/customer_satisfaction_brief.md` | Total feedback volume, weighted insight volume, satisfaction rate, follow-up completion, journey-stage reporting |
| Customer segmentation and profiling | `Customer Segment Scoring` section, `cx-analyst-lab/src/build_cx_summary.py` | Segment categories, scoring components, priority labels, at-risk segment count, actionability logic |
| Trend identification | `Journey Bottlenecks and CX Actions` section, `cx-analyst-lab/data/cx_feedback_sample.csv` | Signals, likely causes, recommended actions, expected impact, monthly trend-ready feedback sample |
| Cross-functional collaboration | `Insight-to-Action Tracker` and `Stakeholder Map` | CX, CRM, dealer, service, product, digital, data/privacy stakeholder handoff logic |
| Excel / BI evidence | `dashboard-workbook/customer_experience_dashboard.xlsx`, `cx-analyst-lab/powerbi/measure_catalog.md`, `cx-analyst-lab/powerbi/star_schema.md` | Dashboard, raw data, pivot summary, at-risk segments, recommendations, DAX-style measures, star-schema notes |
| SQL and reproducible analyst workflow | `cx-analyst-lab/` | CSV validation, KPI build script, SQL reporting views, metric unit tests, customer satisfaction brief |
| Clear communication of complex data | `Customer Insight Brief Simulator`, `Reporting Guide`, `Dashboard MVP Brief` | Structured insight brief, reporting guide, MVP framing, plain-language methodology |
| Responsible customer-data handling | `Customer Data Quality & Privacy Guardrails`, `Methodology` | Simulated-data disclaimer, aggregation/privacy checks, human-review framing |
| AI/data engineering supplement | `industrial-cx-ai-lab/` | Simulated OPC UA-style telemetry, anomaly features, churn/service-risk classifier, SQLite feature mart, Influx export, Grafana panel stub, Slurm batch script |
| Production simulation supplement | `production-sim-stack/` | FastAPI scoring, Docker Compose, MQTT simulation, MLflow-style run metadata, MinIO/S3-style artifact manifest, DuckDB mart SQL, Influx/Grafana monitoring artifacts, Slurm job array |
| Explicit scikit-learn ML baseline | `ml-baseline/` | Train/test split, logistic model, rule baseline, accuracy, precision, recall, F1, confusion matrix, model coefficients |
| SQL / DWH shortcut | `sql/reviewer_service_mart.duckdb.sql` | DuckDB mart with service-risk view, line summary, and anomaly checks |
| HPC / Slurm shortcut | `hpc/run_pipeline.sbatch` | Slurm entrypoint that runs industrial AI, production simulation, MQTT simulator, and ML baseline |

## AI Internship Reviewer Shortcut

| Target signal | Inspect this first | Evidence now present |
| --- | --- | --- |
| BI-REX Industrial AI / IoT | `industrial-cx-ai-lab/`, `production-sim-stack/config/mqtt_topics.json`, `production-sim-stack/src/mqtt_simulator.py` | OPC UA-style nodes, MQTT topics, simulated telemetry, anomaly signals, service-escalation target |
| Grafana / InfluxDB monitoring | `production-sim-stack/docker-compose.yml`, `production-sim-stack/grafana/industrial_service_dashboard.json`, `industrial-cx-ai-lab/artifacts/service_risk_influx.lp` | Docker Compose service definitions, dashboard JSON, Influx line protocol output |
| ML model development | `ml-baseline/train_model.py`, `industrial-cx-ai-lab/src/run_pipeline.py` | scikit-learn logistic baseline, local classifier, metrics, model card, predictions |
| SQL / DWH / analytics engineering | `sql/reviewer_service_mart.duckdb.sql`, `production-sim-stack/sql/service_feature_mart.duckdb.sql` | DuckDB views for service risk, anomaly checks, line summaries, and reviewer decisions |
| HPC / Slurm | `hpc/run_pipeline.sbatch`, `industrial-cx-ai-lab/slurm/run_industrial_cx_model.sbatch`, `production-sim-stack/slurm/run_iot_scoring_array.sbatch` | CPU job script, job array simulation, batch-packaged AI workload |
| PwC / CRIF support evidence | `README.md`, `EVIDENCE_MAP.md`, `ml-baseline/`, `sql/` | Dashboard storytelling plus reproducible ML/SQL evidence |

## Recommended GitHub Repository Metadata

Homepage:

```text
https://errer441122.github.io/ducati-cx-case-study/
```

Topics:

```text
customer-analytics, data-analysis, dashboard, excel, cx, portfolio-project, customer-experience, segmentation, industrial-iot, machine-learning, opc-ua
```

## Interview Framing

> I built a Customer Experience analytics workbook using simulated data to show how I would organize customer signals, report satisfaction trends, segment customers, identify journey friction, and translate findings into action-ready recommendations for CX, CRM, dealer, service, product, and data/privacy stakeholders.

## What Not To Claim

- Do not claim access to Ducati internal systems, customer data, dealer data, or confidential processes.
- Do not claim this is a production Power BI deployment.
- Do claim CX analytics reasoning, Excel/BI readiness, segmentation logic, reporting discipline, and responsible customer-data framing.
