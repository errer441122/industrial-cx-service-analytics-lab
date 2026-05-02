# Evidence Map - Industrial CX and Service Analytics

This file maps target-role requirements to concrete repository evidence. It favors inspectable files, commands, tests and generated artifacts over broad claims.

## Role evidence

| Target role area | Requirement signal | Where to inspect | Evidence shown | Honest gap |
| --- | --- | --- | --- | --- |
| Industrial AI / Data Engineering | Python, ETL, time-series data, MQTT/OPC UA-style contracts, monitoring artifacts | `industrial-cx-ai-lab/`, `production-sim-stack/`, `sql/` | simulated telemetry, topic contracts, line protocol, feature mart, dashboard JSON | No real plant, broker, edge device or production data |
| Applied ML / Anomaly Detection | anomaly scoring, service-risk classifier, model metrics | `industrial-cx-ai-lab/src/`, `ml-baseline/`, artifacts | rule baseline, IsolationForest, service-risk classifier, feature importance | Synthetic labels; no validated industrial dataset |
| CX / Product Analytics | segmentation, KPI logic, stakeholder reporting | workbook, `cx-analyst-lab/`, dashboard artifacts | CX segmentation, KPI reporting, action tracker, SQL-style views | No real customer/dealer data |
| API / MLOps Simulation | local scoring, Docker path, model adapter, smoke tests | `production-sim-stack/` | scoring adapter, FastAPI-compatible API, Docker Compose, generated artifacts | Local simulation only |
| HPC / Batch Packaging | Slurm-ready workload, benchmark, packaging discipline | `hpc/`, `benchmarks/`, `production-sim-stack/slurm/` | local CPU benchmark and Slurm job-array packaging | No real cluster, GPU or scheduler execution |
| Responsible AI / Governance | human review, model limits, no automated decisioning | `docs/reviewer/CLAIMS_AND_LIMITATIONS.md`, policy notes | explicit limitations and reviewer boundaries | Not a certified governance framework or production audit |

## Technical artifact map

| If the reviewer is checking for... | Inspect this first | Evidence shown |
| --- | --- | --- |
| Simulated telemetry fields | `industrial-cx-ai-lab/data/simulated_telemetry.csv` | `timestamp`, `asset_id`, `rpm`, `temperature_c`, `vibration_mm_s`, `pressure_bar`, `torque_nm`, `operating_hours`, `error_code_count`, `service_delay_days`, `customer_satisfaction_score`, `anomaly_label`, `service_escalation_label` |
| Controlled anomaly injection | `industrial-cx-ai-lab/src/telemetry_generator.py` | temperature spike, vibration drift, pressure drop, error burst, delayed maintenance |
| Anomaly metrics | `industrial-cx-ai-lab/artifacts/anomaly_metrics.json` | rule-based baseline and IsolationForest metrics |
| Service-risk classifier | `industrial-cx-ai-lab/artifacts/service_risk_metrics.json` | F1, ROC-AUC, PR-AUC, precision, recall |
| Feature importance | `industrial-cx-ai-lab/artifacts/feature_importance.csv` | reviewer-readable feature ranking |
| Maintenance policy | `industrial-cx-ai-lab/artifacts/maintenance_policy_note.md` | human-in-the-loop use and false positive/negative tradeoff |
| OPC UA / MQTT / Influx / Grafana | `industrial-cx-ai-lab/ops/` | simulated tag map, topic contract, schema, dashboard JSON, Telegraf sample |
| API scoring | `production-sim-stack/src/api.py`, `production-sim-stack/src/model_adapter.py` | `/health`, `/score/service-risk`, `/score/anomaly` when FastAPI is installed; pure-Python scoring otherwise |
| MQTT dry-run | `production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5` | broker-free JSON messages |
| Slurm / benchmark | `hpc/`, `benchmarks/` | job-array packaging and local CPU benchmark JSON |

## Commands

```bash
npm test
python -m pytest -q
python industrial-cx-ai-lab/src/run_pipeline.py
python production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5
python benchmarks/industrial_scoring_benchmark.py --quick
python -m json.tool industrial-cx-ai-lab/ops/opcua_tag_map.json
python -m json.tool industrial-cx-ai-lab/ops/grafana_dashboard.json
```

## What not to claim

- Do not claim access to any company's internal systems, customer data, dealer data, telemetry, dashboards or confidential processes.
- Do not claim real OPC UA, MQTT, InfluxDB, Grafana, Telegraf, Slurm, cloud, edge or production integration.
- Do not claim production predictive maintenance, safety, warranty, pricing or customer-treatment automation.
- Do not claim validated model quality beyond local metrics on synthetic data.
