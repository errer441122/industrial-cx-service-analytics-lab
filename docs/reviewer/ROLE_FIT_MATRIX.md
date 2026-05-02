# Role Fit Matrix

| Target area | Must-have to show | Repo artifacts | Honest gap |
| --- | --- | --- | --- |
| Industrial AI / Data Engineering | Python/bash, ETL, Slurm, Influx/Grafana, OPC UA/MQTT, time-series data | `industrial-cx-ai-lab/`, `industrial-cx-ai-lab/ops/`, `production-sim-stack/`, `hpc/`, `benchmarks/` | No real plant, broker, edge device or production execution |
| Applied ML / Anomaly Detection | anomaly detection, service-risk modelling, model limits | `industrial-cx-ai-lab/src/anomaly_detection.py`, `service_risk_model.py`, metrics artifacts, policy note | No validated equipment data |
| Consulting Data & Analytics | analytics storytelling, stakeholder translation, SQL, dashboard, recommendations | CX workbook, `docs/reviewer/CONSULTING_ANALYTICS_STORY.md`, `sql/`, `cx-analyst-lab/` | No client deployment or real consulting engagement |
| HPC / AI Factory Readiness | Slurm-ready industrial workload, benchmark, data management thinking | `hpc/run_industrial_scoring_array.sbatch`, `benchmarks/industrial_scoring_benchmark.py`, benchmark JSON | No real cluster, GPU or scheduler execution |
| Responsible AI / Model Evidence | data quality, scoring, transparent limits, human-review boundary | `ml-baseline/`, `production-sim-stack/src/model_adapter.py`, `docs/reviewer/CLAIMS_AND_LIMITATIONS.md` | Portfolio evidence only; not a certified governance framework |

Use this repository primarily as industrial analytics, applied ML, CX analytics and reviewer-facing model-evidence support.
