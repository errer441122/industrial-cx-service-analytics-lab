# BI-REX Industrial Story

This repository is positioned as secondary but strong evidence for industrial analytics and industrial AI support roles. It is built around local simulation, not real plant integration.

## Industrial Data Path

1. `industrial-cx-ai-lab/src/telemetry_generator.py` creates deterministic synthetic telemetry.
2. `industrial-cx-ai-lab/src/feature_engineering.py` creates rule features and rolling telemetry features.
3. `industrial-cx-ai-lab/src/anomaly_detection.py` evaluates rule-based anomaly detection and IsolationForest.
4. `industrial-cx-ai-lab/src/service_risk_model.py` trains/evaluates a service-risk classifier.
5. `industrial-cx-ai-lab/ops/` documents simulated OPC UA, MQTT, Influx, Grafana, and Telegraf artifacts.
6. `hpc/run_industrial_scoring_array.sbatch` and `benchmarks/` show batch packaging and local CPU timing.

## Why It Fits BI-REX Screening

| Signal | Evidence |
| --- | --- |
| Time-series industrial data | simulated telemetry CSV and line protocol export |
| OPC UA / MQTT awareness | tag map and topic contract |
| Influx/Grafana awareness | schema and dashboard JSON |
| Predictive maintenance direction | anomaly metrics and maintenance policy note |
| HPC / Slurm packaging | job-array script and local benchmark |

## Boundary

No real BI-REX, IPAZIA, Ducati, plant, edge, cloud, MQTT broker, OPC UA server, InfluxDB, Grafana, or Slurm execution is claimed.
