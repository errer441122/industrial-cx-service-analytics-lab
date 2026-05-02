# Production Simulation Architecture

This is a local-only production-style simulation for reviewer inspection. It does not claim real company systems, dealer data, plant telemetry, OPC UA, MQTT, InfluxDB, Grafana, Slurm, cloud, or edge deployment.

## Components

| Component | File / artifact | Executed locally |
| --- | --- | --- |
| FastAPI-compatible scoring | `src/api.py`, `src/model_adapter.py` | Importable and testable; server run is optional. |
| Service-risk rules | `src/model_adapter.py` | Yes, through unit tests and optional API example. |
| Anomaly rules | `src/model_adapter.py` | Yes, through unit tests and optional API example. |
| MQTT dry-run | `src/mqtt_simulator.py` | Yes, writes JSONL or prints dry-run messages. |
| Lifecycle artifacts | `src/orchestrate.py`, `artifacts/mlflow_run.json` | Local JSON only; no real MLflow service required. |
| Object storage design | `artifacts/minio_manifest.json`, `docker-compose.yml` | Manifest only unless Docker is run manually. |
| Time-series output | `artifacts/industrial_service_influx.lp` | Local line-protocol file only. |
| Grafana design | `grafana/industrial_service_dashboard.json` | Design artifact only unless Docker is run manually. |
| Slurm job array | `slurm/run_iot_scoring_array.sbatch` | Packaging only; no real cluster execution. |

## Data Flow

1. `data/iot_stream_seed.csv` provides a small synthetic industrial-service stream.
2. `src/pipeline.py` scores rows with a transparent local baseline.
3. `src/orchestrate.py` writes predictions, SQLite mart, line protocol, MQTT JSONL, and lifecycle metadata.
4. `src/api.py` exposes local scoring functions and optional FastAPI endpoints.
5. `src/mqtt_simulator.py --dry-run --messages 5` prints broker-free MQTT-style messages.

## API Surface

Minimum endpoints when FastAPI is installed:

- `GET /health`
- `POST /score/service-risk`
- `POST /score/anomaly`

Pure-Python scoring remains available through:

- `src/model_adapter.py`
- `src/api.py --example`

## Failure Modes And Limits

- The scoring baseline is deterministic and not validated against real industrial failures.
- Docker Compose is optional and may fail if Docker is unavailable.
- Grafana, InfluxDB, MLflow, and MinIO files are local design or manifest evidence unless their services are explicitly started and smoke-tested.
- No authentication, authorization, network security, secrets management, retention policy, or safety certification is implemented.

## What Production Would Require

Real production use would require approved data access, validated data contracts, broker/server credentials, monitoring, alert routing, security review, safety review, model validation, human operating procedures, incident management, and deployment evidence from the target environment.
