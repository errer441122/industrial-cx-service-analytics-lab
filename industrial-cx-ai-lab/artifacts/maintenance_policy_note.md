# Maintenance Policy Note

This note summarizes a simulated industrial CX and service analytics workflow. It uses synthetic telemetry and service labels only; it is not connected to company systems, dealer systems, production equipment, OPC UA servers, MQTT brokers, InfluxDB, Grafana, Slurm, cloud, or edge infrastructure.

## What The Lab Flags

- Rule-based anomaly screening flags high temperature, high vibration, pressure drops, error bursts, and delayed maintenance.
- The IsolationForest path adds an unsupervised anomaly benchmark against controlled synthetic labels.
- The service-risk classifier estimates whether a telemetry/service row should be reviewed by a human service owner.

## Current Local Metrics

- Rule-based anomaly F1: `0.8529`
- IsolationForest anomaly F1: `0.8462`
- Service-risk classifier F1: `0.9333`
- Service-risk ROC-AUC: `1.0`
- Service-risk PR-AUC: `1.0`

## Human-In-The-Loop Use

Use model output as a queueing signal for a service analyst or industrial data reviewer. A high score should trigger inspection of the telemetry trace, related customer feedback, open service delays, and operational context. It must not automatically trigger warranty action, safety action, customer treatment, pricing, or dealer performance conclusions.

## False Positive / False Negative Tradeoff

False positives waste reviewer time but can be acceptable in a triage queue. False negatives are more serious because they may hide a deteriorating asset or unresolved customer/service issue. Thresholds should be tuned with validated operating data before any real use.

## Industrial AI / HPC Relevance

The local pipeline mirrors the shape of an industrial analytics proof of concept: time-series ingestion, protocol mapping, anomaly scoring, service-risk classification, Influx/Grafana-style monitoring artifacts, and Slurm-ready batch packaging. The evidence here is packaging and local CPU execution only, not a real cluster, partner, employer or production run.
