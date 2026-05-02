from __future__ import annotations

import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "iot_stream_seed.csv"
SERVICE_ESCALATION_THRESHOLD = 0.45

RISK_TERMS = {
    "breakdown",
    "complaint",
    "critical",
    "delay",
    "delayed",
    "escalation",
    "fault",
    "overheating",
    "repeat",
    "unresolved",
    "vibration",
    "warning",
}


def _float(value: str, column: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{column} must be numeric, got {value!r}") from exc


def _int(value: str, column: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{column} must be an integer, got {value!r}") from exc


def load_events(path: Path = DATA_PATH) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = []
        for raw in csv.DictReader(handle):
            rows.append(
                {
                    "event_id": raw["event_id"],
                    "line": raw["line"],
                    "asset_family": raw["asset_family"],
                    "timestamp": raw["timestamp"],
                    "opcua_node": raw["opcua_node"],
                    "vibration_rms": _float(raw["vibration_rms"], "vibration_rms"),
                    "temperature_c": _float(raw["temperature_c"], "temperature_c"),
                    "battery_voltage": _float(raw["battery_voltage"], "battery_voltage"),
                    "oil_pressure_bar": _float(raw["oil_pressure_bar"], "oil_pressure_bar"),
                    "service_delay_days": _int(raw["service_delay_days"], "service_delay_days"),
                    "nps": _int(raw["nps"], "nps"),
                    "warranty_claims": _int(raw["warranty_claims"], "warranty_claims"),
                    "telemetry_dropouts": _int(raw["telemetry_dropouts"], "telemetry_dropouts"),
                    "mqtt_topic": raw["mqtt_topic"],
                    "customer_note": raw["customer_note"],
                    "service_escalation": _int(raw["service_escalation"], "service_escalation"),
                }
            )
    if len(rows) < 20:
        raise ValueError("Expected at least 20 industrial stream rows.")
    return rows


def count_text_risk_hits(text: str) -> int:
    tokens = {token.strip(".,:;()[]").lower() for token in text.split()}
    return len(tokens & RISK_TERMS)


def score_event(event: dict[str, object]) -> float:
    vibration = min(1.0, max(0.0, (float(event["vibration_rms"]) - 2.0) / 4.0))
    temperature = min(1.0, max(0.0, (float(event["temperature_c"]) - 82.0) / 22.0))
    battery = min(1.0, max(0.0, (12.6 - float(event["battery_voltage"])) / 1.2))
    oil_pressure = min(1.0, max(0.0, (3.0 - float(event["oil_pressure_bar"])) / 1.5))
    service_delay = min(1.0, float(event["service_delay_days"]) / 25.0)
    nps_risk = min(1.0, max(0.0, (8.0 - float(event["nps"])) / 8.0))
    claims = min(1.0, float(event["warranty_claims"]) / 3.0)
    dropouts = min(1.0, float(event["telemetry_dropouts"]) / 3.0)
    text_risk = min(1.0, count_text_risk_hits(str(event["customer_note"])) / 4.0)

    probability = (
        0.12 * vibration
        + 0.12 * temperature
        + 0.09 * battery
        + 0.10 * oil_pressure
        + 0.15 * service_delay
        + 0.12 * nps_risk
        + 0.12 * claims
        + 0.08 * dropouts
        + 0.10 * text_risk
    )
    return round(min(max(probability, 0.0), 1.0), 4)


def score_events(events: list[dict[str, object]]) -> list[dict[str, object]]:
    scored = []
    for event in events:
        probability = score_event(event)
        scored.append(
            {
                **event,
                "text_risk_hits": count_text_risk_hits(str(event["customer_note"])),
                "predicted_service_escalation_probability": probability,
                "predicted_service_escalation": int(probability >= SERVICE_ESCALATION_THRESHOLD),
            }
        )
    return scored


def evaluate(scored: list[dict[str, object]]) -> dict[str, float]:
    labels = [int(row["service_escalation"]) for row in scored]
    predictions = [int(row["predicted_service_escalation"]) for row in scored]
    tp = sum(1 for expected, actual in zip(labels, predictions) if expected == 1 and actual == 1)
    tn = sum(1 for expected, actual in zip(labels, predictions) if expected == 0 and actual == 0)
    fp = sum(1 for expected, actual in zip(labels, predictions) if expected == 0 and actual == 1)
    fn = sum(1 for expected, actual in zip(labels, predictions) if expected == 1 and actual == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": round((tp + tn) / len(labels), 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }
