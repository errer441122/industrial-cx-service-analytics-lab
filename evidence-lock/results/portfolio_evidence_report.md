# Portfolio Evidence Report

Generated at: 2026-05-02T21:59:44+00:00

## Executive Summary

This Evidence Lock makes the repository reviewable as an industrial Python/data-engineering portfolio project, not only as a static CX workbook. The workbook remains the communication layer; the durable evidence is telemetry generation, anomaly and service-risk scoring, MQTT dry-run output, Influx line protocol, feature-mart artifacts, API smoke evidence, Docker Compose packaging, and CPU benchmark output.

## Reproducibility

```bash
make setup
make evidence
```

Equivalent shell steps are listed in `evidence-lock/commands.sh`.

## Industrial Service Risk Evidence

| Evidence | Value |
| --- | --- |
| Service-risk F1 | 0.9333 |
| Service-risk ROC-AUC | 1.0 |
| Anomaly rule F1 | 0.8529 |
| Production-sim rows | 20 |
| API smoke probability | 0.4142 |
| Local benchmark rows/sec | 125.33 |

## Industrial Stack Evidence

| Artifact | Path |
| --- | --- |
| Docker smoke note | `industrial-evidence-lock/docker_smoke_test.md` |
| Grafana service screenshot | `industrial-evidence-lock/grafana_screenshot.png` |
| Grafana dashboard JSON | `industrial-evidence-lock/grafana_dashboard.json` |
| Influx line protocol sample | `industrial-evidence-lock/influx_line_protocol_sample.lp` |
| MQTT terminal log | `industrial-evidence-lock/mqtt_terminal_log.txt` |
| API prediction log | `industrial-evidence-lock/api_prediction_log.txt` |
| Feature mart output | `industrial-evidence-lock/feature_mart_duckdb_output.md` |

## Scope Boundaries

This is not a company system, not a production industrial integration, not a real dealer/customer dataset, not a warranty/safety/pricing decision tool, and not a real partner, employer, client, cluster or production deployment.
