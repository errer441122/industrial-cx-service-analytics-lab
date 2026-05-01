# AI Internship Fit Review

This repository is still not the primary AI internship project, but it is no longer dashboard-only. Use it as secondary evidence for analytics communication, customer data reasoning, segmentation, Industrial IoT-style data engineering, lightweight ML, and stakeholder translation.

## Best Use

Frame this project as:

> A customer experience analytics workbook using simulated data to show how I structure data collection, segmentation, satisfaction reporting, insight communication, and action tracking.

For technical reviewers, add:

> I extended the workbook with an Industrial CX AI lab using simulated OPC UA-style telemetry, anomaly features, text-risk features, a churn/service-risk classifier, SQLite feature mart, Influx export, Grafana stub, and Slurm batch script.

Also show `production-sim-stack/` if the role asks for industrial AI, MLOps, APIs, or infrastructure thinking. It adds FastAPI scoring, Docker Compose, MQTT simulation, MLflow-style run metadata, MinIO/S3-style artifact layout, DuckDB SQL, Influx/Grafana monitoring artifacts, and Slurm job array.

The top-level `ml-baseline/`, `sql/`, and `hpc/` folders exist so a technical reviewer can quickly verify conventional scikit-learn model development, DWH-style SQL, and Slurm packaging without digging through the larger labs.

## Fit Against AI/Data Targets

| Target | Fit | Why |
| --- | --- | --- |
| CRIF | Medium-high | Shows data-quality thinking, text-risk features, scoring API, scikit-learn baseline, and transparent model limits. Still weaker than the governance repo for regulated AI. |
| PwC | High | Stronger now: dashboard/storytelling plus executable ML lab, top-level DuckDB SQL, API, Docker path, feature mart, model card, lifecycle artifacts, and CI validation. |
| UNDP | Low-medium | Responsible data handling is relevant, but the business context is still not development, humanitarian, or public-sector analytics. |
| CINECA / IT4LIA | Medium-high | Adds Slurm-ready job array, Docker path, packaged AI workload, and monitoring artifacts, but still no real cluster/GPU/JupyterHub execution. |
| BI-REX | High | Adds simulated OPC UA/Kepware-style telemetry, MQTT stream simulation, industrial anomaly signals, Influx/Grafana artifacts, MinIO/S3-style artifact layout, and Slurm-style run path. |

## What To Show

- `EVIDENCE_MAP.md` for requirement-to-artifact mapping.
- `dashboard-workbook/customer_experience_dashboard.xlsx` for Excel/BI readiness.
- `scripts/validate-data.mjs` and `.github/workflows/validate.yml` for basic reproducibility.
- `ml-baseline/train_model.py` for conventional scikit-learn model evidence.
- `sql/reviewer_service_mart.duckdb.sql` for top-level SQL/DWH evidence.
- `hpc/run_pipeline.sbatch` for top-level Slurm evidence.
- `industrial-cx-ai-lab/src/run_pipeline.py` for ML, feature engineering, and artifact generation.
- `industrial-cx-ai-lab/ops/kepware_tag_map.json` and `industrial-cx-ai-lab/ops/grafana_panel.json` for BI-REX-style industrial monitoring context.
- `industrial-cx-ai-lab/slurm/run_industrial_cx_model.sbatch` for HPC-style batch packaging.
- `production-sim-stack/src/api.py`, `production-sim-stack/docker-compose.yml`, and `production-sim-stack/src/mqtt_simulator.py` for production-like industrial AI evidence.
- The live workbook for communication and product thinking.

## Do Not Claim

- Do not claim access to Ducati systems or customer data.
- Do not claim production Power BI deployment.
- Do not present this as a production AI engineering project.
- Do not claim real OPC UA, Kepware, InfluxDB, Grafana, Slurm, cloud, or Ducati telemetry integration.
- Do not claim the production simulation stack is a real production deployment.
- Do not use this as the first portfolio link for CRIF or UNDP. It can be a strong first link for BI-REX-style industrial AI roles if paired with the lab folders.

## Best Next Improvement

The best next improvement is no longer another local simulation. The next meaningful step would be real external execution evidence:

- run the Docker Compose stack and capture smoke-test output;
- add a real public industrial or open mobility dataset;
- add a real MLflow run if dependencies are installed;
- add Spark or Dask for a larger-data path;
- run the Slurm scripts on a real cluster if access becomes available.
