# Production Simulation Stack

This folder is the `8/10` upgrade layer for BI-REX, PwC, CINECA/IT4LIA, and industrial AI screening.

It turns the CX workbook into a production-like industrial analytics simulation: API scoring, MQTT/OPC UA-style events, MLflow-style tracking, MinIO/S3-style artifact layout, DuckDB mart SQL, Influx line protocol, Grafana dashboard, and Slurm batch entrypoint.

It uses simulated data only. No Ducati system, customer, dealer, motorcycle, telemetry, or production plant data is represented.

## What This Adds

| Gap | Evidence in this folder |
| --- | --- |
| FastAPI scoring endpoint | `src/api.py` |
| Docker path | `Dockerfile`, `docker-compose.yml` |
| MQTT/OPC UA-style data | `data/iot_stream_seed.csv`, `config/mqtt_topics.json`, `src/mqtt_simulator.py` |
| MLflow-style lifecycle | `src/orchestrate.py`, generated `artifacts/mlflow_run.json` |
| MinIO/S3-style storage | `docker-compose.yml`, generated `artifacts/minio_manifest.json` |
| DuckDB/dbt-style mart | `sql/service_feature_mart.duckdb.sql` |
| Grafana/Influx monitoring | `grafana/industrial_service_dashboard.json`, generated line protocol |
| HPC/Slurm path | `slurm/run_iot_scoring_array.sbatch` |

## Local Validation

From the repository root:

```bash
python3 -m unittest discover production-sim-stack/tests
python3 production-sim-stack/src/orchestrate.py
python3 production-sim-stack/src/mqtt_simulator.py
```

Optional service run, if Docker and dependencies are available:

```bash
cd production-sim-stack
docker compose up --build
```

## Reviewer Boundary

The model is advisory. It flags service records for human review. It does not automate customer treatment, warranty decisions, safety decisions, pricing, or commercial action.
