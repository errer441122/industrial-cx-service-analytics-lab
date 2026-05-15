# Evidence Map - Industrial CX Service Analytics Lab

This file maps target-role requirements to concrete repository evidence. It favors inspectable files, commands, tests, and generated artifacts over broad claims.

Positioning: this is the industrial service-analytics and Data & AI consulting case in the portfolio. It should be presented as executable evidence for telemetry-to-decision translation, not as a production plant deployment and not as the flagship regulated AI governance project.

## Role Evidence

| Target role / employer type | Requirement signal | Where to inspect it | Evidence shown | Honest gap |
| --- | --- | --- | --- | --- |
| industrial innovation Data Engineer | Python/bash, ETL, time-series data, OPC UA/MQTT, Influx/Grafana, Slurm | `industrial-cx-ai-lab/`, `industrial-cx-ai-lab/ops/`, `production-sim-stack/`, `hpc/`, `benchmarks/` | simulated telemetry, tag map, topic contract, line protocol, dashboard JSON, dry-run MQTT, Slurm array, local CPU benchmark | No real plant, broker, edge, industrial innovation, industrial pilot, or production execution |
| industrial innovation AI Engineer | anomaly detection, predictive maintenance direction, service-risk ML | `industrial-cx-ai-lab/src/anomaly_detection.py`, `service_risk_model.py`, artifacts JSON/CSV/MD | rule baseline, IsolationForest, RandomForest service-risk classifier, feature importance, policy note | Synthetic labels and no validated industrial data |
| Data & AI Consulting | dashboard storytelling, stakeholder communication, SQL, recommendations, responsible score-to-action boundaries | workbook, `cx-analyst-lab/`, `sql/`, `docs/reviewer/CONSULTING_DATA_AI_STORY.md`, `docs/reviewer/CX_TO_INDUSTRIAL_AI_BRIDGE.md` | CX segmentation, KPI reporting, action tracker, SQL/DWH shortcut, telemetry-to-service bridge, service-risk model evidence, communication note | No client deployment |
| HPC / AI Factory | Slurm-ready workload, benchmark, packaging discipline | `hpc/run_industrial_scoring_array.sbatch`, `benchmarks/industrial_scoring_benchmark.py`, benchmark artifact | local CPU benchmark and Slurm job-array packaging | No cluster, GPU, national HPC cluster, or AI Factory execution |
| financial-services support evidence | data quality, transparent scoring, model limits | `scripts/validate-data.mjs`, `ml-baseline/`, `production-sim-stack/src/model_adapter.py` | validation, model boundary, dependency-light scoring adapter | Support evidence only, no financial-services data |
| public-sector support evidence | responsible data communication | `docs/reviewer/CLAIMS_AND_LIMITATIONS.md`, maintenance policy note | human review and no automated decision boundary | Context is not development/humanitarian |

## Technical Artifact Map

| If the reviewer is checking for... | Inspect this first | Evidence now present |
| --- | --- | --- |
| Simulated telemetry fields | `industrial-cx-ai-lab/data/simulated_telemetry.csv` | `timestamp`, `asset_id`, `rpm`, `temperature_c`, `vibration_mm_s`, `pressure_bar`, `torque_nm`, `operating_hours`, `error_code_count`, `service_delay_days`, `customer_satisfaction_score`, `anomaly_label`, `service_escalation_label` |
| Controlled anomaly injection | `industrial-cx-ai-lab/src/telemetry_generator.py` | temperature spike, vibration drift, pressure drop, error burst, delayed maintenance |
| Anomaly metrics | `industrial-cx-ai-lab/artifacts/anomaly_metrics.json` | rule-based baseline and IsolationForest metrics |
| Service-risk classifier | `industrial-cx-ai-lab/artifacts/service_risk_metrics.json` | F1, ROC-AUC, PR-AUC, precision, recall |
| Feature importance | `industrial-cx-ai-lab/artifacts/feature_importance.csv` | reviewer-readable feature ranking |
| Maintenance policy | `industrial-cx-ai-lab/artifacts/maintenance_policy_note.md` | human-in-the-loop use, false positive/negative tradeoff, industrial innovation relevance |
| OPC UA / MQTT / Influx / Grafana | `industrial-cx-ai-lab/ops/` | simulated tag map, topic contract, schema, dashboard JSON, Telegraf sample |
| API scoring | `production-sim-stack/src/api.py`, `src/model_adapter.py` | `/health`, `/score/service-risk`, `/score/anomaly` when FastAPI is installed; pure-Python scoring otherwise |
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

## What Not To Claim

- Do not claim access to premium mobility brand internal systems, customer data, dealer data, telemetry, dashboards, or confidential processes.
- Do not claim real OPC UA/Kepware/MQTT/Influx/Grafana/Telegraf/Slurm/cloud/edge integration.
- Do not claim production predictive maintenance, safety, warranty, pricing, or customer-treatment automation.
