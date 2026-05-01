# Docker Smoke Test

Executed locally from production-sim-stack/ after docker compose up -d --build.

| Check | Result |
| --- | --- |
| FastAPI /health | `{"status":"ok","mode":"local_simulation","disclaimer":"Simulation only; not a production industrial decision system."}` |
| FastAPI /score/service-risk | `{"asset_id":"line-01-pump-01","risk_score":0.4142,"risk_band":"low","human_review_required":false,"model_source":"local_simulated_baseline","disclaimer":"Simulation only; not a production industrial decision system.","event_id":"line-01-pump-01","bike_family":"synthetic-industrial-asset","predicted_service_escalation_probability":0.4142,"predicted_service_escalation":0,"decision_boundary":"advisory human-review triage only"}` |
| Grafana /api/health | `{
  "database": "ok",
  "version": "11.3.0",
  "commit": "d9455ff7db73b694db7d412e49a68bec767f2b5a"
}` |
| InfluxDB /health | `{"name":"influxdb", "message":"ready for queries and writes", "status":"pass", "checks":[], "version": "v2.7.12", "commit": "ec9dcde5d6"}
` |
| MLflow /health | `OK` |
| MinIO live health | `200` |

Boundary: local Docker Compose smoke only; not a production industrial deployment.
