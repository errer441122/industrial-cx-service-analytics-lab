# Smoke Test Plan

This plan distinguishes local checks that were executed from optional service checks that require Docker or external infrastructure. No real Ducati, plant, dealer, cloud, Slurm, OPC UA, MQTT, InfluxDB, or Grafana integration is claimed.

## Executed Local Checks

Run from the repository root:

```bash
python -m pytest -q production-sim-stack/tests
python production-sim-stack/src/orchestrate.py
python production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5
python production-sim-stack/src/api.py --example
```

These checks validate importable scoring functions, lifecycle artifact generation, and broker-free MQTT-style payloads.

## Planned Optional Docker Checks

Only run if Docker is available:

```bash
cd production-sim-stack
docker compose up --build
```

Optional endpoints to inspect after startup:

- FastAPI `/health`
- FastAPI `/score/service-risk`
- FastAPI `/score/anomaly`
- Grafana local service health
- InfluxDB local service health
- MinIO local service health

## Not Executed By Default

- Real MQTT broker publish/subscribe.
- Real OPC UA server reads.
- Real InfluxDB writes from Telegraf.
- Real Grafana dashboard import.
- Real MLflow tracking server registration.
- Real MinIO uploads.
- Real Slurm submission.

Reviewer boundary: default tests are CPU-only and offline. Service checks require local tooling and should be recorded separately if executed.
