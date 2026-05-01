# AI Internship Fit Review

This repository is secondary but strong evidence for industrial analytics, industrial AI support, and analytics communication. It should not be presented as the main CRIF or UNDP AI engineering project.

## Best Use

Frame this project as:

> An industrial CX and service analytics case study using simulated data: customer analytics workbook plus synthetic telemetry generation, anomaly detection, service-risk scoring, MQTT/OPC UA-style design artifacts, Influx/Grafana files, FastAPI-compatible scoring, DuckDB SQL, and Slurm-ready batch packaging.

## Company Fit

| Target | Fit | Evidence to show | Gap to acknowledge |
| --- | --- | --- | --- |
| BI-REX Data Engineer | High | `industrial-cx-ai-lab/`, `ops/opcua_tag_map.json`, `ops/mqtt_topics.json`, Influx/Grafana artifacts, `production-sim-stack/`, `hpc/`, `benchmarks/` | No real plant, broker, OPC UA, Influx, Grafana, edge, or IPAZIA run |
| BI-REX AI Engineer | Medium-high | anomaly metrics, IsolationForest baseline, service-risk classifier, feature importance, maintenance policy note | No deep learning/CV and no validated equipment data |
| PwC Data & AI | High | CX workbook, action tracker, SQL, model communication note, `docs/reviewer/PWC_ANALYTICS_STORY.md` | No client delivery or production BI deployment |
| CINECA / IT4LIA | Medium | Slurm-ready array, Docker/local stack docs, local CPU benchmark | No real cluster, GPU, Leonardo, or AI Factory execution |
| CRIF | Medium | transparent scoring boundaries, data validation, `ml-baseline/`, service-risk model | Secondary evidence; no real CRIF data or regulated credit model |
| UNDP | Low-medium | responsible data and human-review boundaries | Business context is not public-sector development or humanitarian analytics |

## What To Show

- `docs/reviewer/RECRUITER_5_MIN_ROUTE.md` for quick navigation.
- `docs/reviewer/TECHNICAL_20_MIN_ROUTE.md` for commands and artifacts.
- `industrial-cx-ai-lab/artifacts/anomaly_metrics.json` for anomaly evidence.
- `industrial-cx-ai-lab/artifacts/service_risk_metrics.json` for classifier evidence.
- `industrial-cx-ai-lab/artifacts/maintenance_policy_note.md` for communication and human-review framing.
- `industrial-cx-ai-lab/ops/` for simulated industrial protocol and monitoring artifacts.
- `production-sim-stack/src/api.py` and `src/model_adapter.py` for local scoring evidence.
- `benchmarks/artifacts/local_cpu_benchmark.json` for local CPU benchmark evidence.

## Do Not Claim

- Do not claim access to Ducati systems, Ducati customer data, dealer data, telemetry, dashboards, or internal processes.
- Do not claim real OPC UA, Kepware, MQTT, InfluxDB, Grafana, Telegraf, Slurm, cloud, edge, BI-REX, IPAZIA, CINECA, IT4LIA, or Ducati execution.
- Do not claim production predictive maintenance, warranty automation, safety automation, or customer-treatment automation.
- Do not claim this as the primary AI engineering project for CRIF or UNDP.

## Next Honest Improvements

- Run Docker Compose locally and record smoke evidence if Docker is available.
- Add an open industrial dataset with source and limitations if a suitable dataset is chosen.
- Run Slurm scripts only if real cluster access becomes available, then commit logs separately with environment details.
