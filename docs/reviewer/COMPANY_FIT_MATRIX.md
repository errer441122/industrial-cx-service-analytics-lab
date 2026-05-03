# Company Fit Matrix

| Target | Must-have to show | Repo artifacts | Honest gap |
| --- | --- | --- | --- |
| BI-REX Data Engineer | Python/bash, ETL, Slurm, Influx/Grafana, OPC UA/MQTT, time-series data | `industrial-cx-ai-lab/`, `industrial-cx-ai-lab/ops/`, `production-sim-stack/`, `hpc/`, `benchmarks/` | No real plant, broker, edge, or BI-REX/IPAZIA execution |
| BI-REX AI Engineer | anomaly detection, predictive maintenance, service-risk modelling, model limits | `industrial-cx-ai-lab/src/anomaly_detection.py`, `service_risk_model.py`, metrics artifacts, policy note | No deep learning, computer vision, or validated equipment data |
| PwC Data & AI | analytics storytelling, stakeholder translation, SQL, dashboard, recommendations | CX workbook, `docs/reviewer/CONSULTING_DATA_AI_STORY.md`, `sql/`, `cx-analyst-lab/` | No client deployment or real consulting engagement |
| CINECA / IT4LIA | Slurm-ready industrial workload, benchmark, data management thinking | `hpc/run_industrial_scoring_array.sbatch`, `benchmarks/industrial_scoring_benchmark.py`, benchmark JSON | No real cluster, GPU, Leonardo, or AI Factory access |
| CRIF | data quality, scoring, transparent limits, service-risk framing | `ml-baseline/`, `production-sim-stack/src/model_adapter.py`, `EVIDENCE_MAP.md` | Secondary evidence only; regulated governance repo is stronger |
| UNDP | responsible data communication and human-review boundary | `docs/reviewer/CLAIMS_AND_LIMITATIONS.md`, policy note | Business context is not development or humanitarian analytics |

Use this repository primarily for BI-REX and PwC-style industrial analytics communication. Use the regulated governance repository as the main CRIF/UNDP/regulated AI engineering evidence.
