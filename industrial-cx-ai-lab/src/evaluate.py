from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def write_json(payload: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def write_feature_importance(rows: list[dict[str, object]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["feature", "importance"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def write_influx_line_protocol(rows: list[dict[str, object]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for row in rows:
        timestamp_ns = int(
            datetime.fromisoformat(str(row["timestamp"]).replace("Z", "+00:00")).timestamp()
            * 1_000_000_000
        )
        tags = f"asset_id={row['asset_id']}"
        fields = (
            f"rpm={int(float(row['rpm']))}i,"
            f"temperature_c={float(row['temperature_c'])},"
            f"vibration_mm_s={float(row['vibration_mm_s'])},"
            f"pressure_bar={float(row['pressure_bar'])},"
            f"torque_nm={float(row['torque_nm'])},"
            f"operating_hours={float(row['operating_hours'])},"
            f"error_code_count={int(row['error_code_count'])}i,"
            f"service_delay_days={int(row['service_delay_days'])}i,"
            f"anomaly_label={int(row['anomaly_label'])}i,"
            f"service_escalation_label={int(row['service_escalation_label'])}i"
        )
        lines.append(f"industrial_service_telemetry,{tags} {fields} {timestamp_ns}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_policy_note(
    anomaly_metrics: dict[str, Any],
    service_metrics: dict[str, Any],
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"""# Maintenance Policy Note

This note summarizes a simulated industrial CX and service analytics workflow. It uses synthetic telemetry and service labels only; it is not connected to Ducati systems, dealer systems, production equipment, OPC UA servers, MQTT brokers, InfluxDB, Grafana, Slurm, cloud, or edge infrastructure.

## What The Lab Flags

- Rule-based anomaly screening flags high temperature, high vibration, pressure drops, error bursts, and delayed maintenance.
- The IsolationForest path adds an unsupervised anomaly benchmark against controlled synthetic labels.
- The service-risk classifier estimates whether a telemetry/service row should be reviewed by a human service owner.

## Current Local Metrics

- Rule-based anomaly F1: `{anomaly_metrics["rule_based"]["f1"]}`
- IsolationForest anomaly F1: `{anomaly_metrics["isolation_forest"]["f1"]}`
- Service-risk classifier F1: `{service_metrics["f1"]}`
- Service-risk ROC-AUC: `{service_metrics["roc_auc"]}`
- Service-risk PR-AUC: `{service_metrics["pr_auc"]}`

## Human-In-The-Loop Use

Use model output as a queueing signal for a service analyst or industrial data reviewer. A high score should trigger inspection of the telemetry trace, related customer feedback, open service delays, and operational context. It must not automatically trigger warranty action, safety action, customer treatment, pricing, or dealer performance conclusions.

## False Positive / False Negative Tradeoff

False positives waste reviewer time but can be acceptable in a triage queue. False negatives are more serious because they may hide a deteriorating asset or unresolved customer/service issue. Thresholds should be tuned with validated operating data before any real use.

## BI-REX / IPAZIA / HPC Relevance

The local pipeline mirrors the shape of a BI-REX-style industrial analytics PoC: time-series ingestion, protocol mapping, anomaly scoring, service-risk classification, Influx/Grafana-style monitoring artifacts, and Slurm-ready batch packaging. The evidence here is packaging and local CPU execution only, not a real BI-REX, IPAZIA, CINECA, or IT4LIA run.
"""
    path.write_text(text, encoding="utf-8")
    return path
