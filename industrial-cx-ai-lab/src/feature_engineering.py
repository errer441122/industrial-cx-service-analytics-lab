from __future__ import annotations

import csv
from collections import defaultdict, deque
from pathlib import Path
from statistics import mean

from telemetry_generator import EXPECTED_FIELDS


NUMERIC_FIELDS = {
    "rpm",
    "temperature_c",
    "vibration_mm_s",
    "pressure_bar",
    "torque_nm",
    "operating_hours",
    "customer_satisfaction_score",
}

INTEGER_FIELDS = {
    "error_code_count",
    "service_delay_days",
    "anomaly_label",
    "service_escalation_label",
}

MODEL_FEATURES = [
    "rpm",
    "temperature_c",
    "vibration_mm_s",
    "pressure_bar",
    "torque_nm",
    "operating_hours",
    "error_code_count",
    "service_delay_days",
    "customer_satisfaction_score",
    "temperature_over_85",
    "vibration_over_5",
    "pressure_under_2",
    "error_burst_flag",
    "maintenance_delay_flag",
    "vibration_rolling_4",
    "temperature_delta_c",
    "service_rule_score",
]


def load_telemetry(path: Path) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = set(EXPECTED_FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing telemetry columns: {sorted(missing)}")

        rows: list[dict[str, object]] = []
        for raw in reader:
            row: dict[str, object] = {
                "timestamp": raw["timestamp"],
                "asset_id": raw["asset_id"],
            }
            for field in NUMERIC_FIELDS:
                row[field] = float(raw[field])
            for field in INTEGER_FIELDS:
                row[field] = int(raw[field])
            rows.append(row)
    return rows


def build_feature_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    if not rows:
        raise ValueError("Cannot build features from an empty telemetry dataset.")

    history: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=4))
    previous_temperature: dict[str, float] = {}
    features: list[dict[str, object]] = []

    for row in sorted(rows, key=lambda item: (str(item["asset_id"]), str(item["timestamp"]))):
        asset_id = str(row["asset_id"])
        vibration_window = history[asset_id]
        vibration_window.append(float(row["vibration_mm_s"]))
        previous_temp = previous_temperature.get(asset_id, float(row["temperature_c"]))

        temperature_over_85 = int(float(row["temperature_c"]) >= 85.0)
        vibration_over_5 = int(float(row["vibration_mm_s"]) >= 5.0)
        pressure_under_2 = int(float(row["pressure_bar"]) <= 2.0)
        error_burst = int(int(row["error_code_count"]) >= 3)
        delay_flag = int(int(row["service_delay_days"]) >= 10)
        satisfaction_risk = max(0.0, (8.0 - float(row["customer_satisfaction_score"])) / 7.0)

        rule_score = min(
            1.0,
            0.22 * temperature_over_85
            + 0.22 * vibration_over_5
            + 0.18 * pressure_under_2
            + 0.18 * error_burst
            + 0.14 * delay_flag
            + 0.06 * satisfaction_risk,
        )

        next_row = {
            **row,
            "temperature_over_85": temperature_over_85,
            "vibration_over_5": vibration_over_5,
            "pressure_under_2": pressure_under_2,
            "error_burst_flag": error_burst,
            "maintenance_delay_flag": delay_flag,
            "vibration_rolling_4": round(mean(vibration_window), 4),
            "temperature_delta_c": round(float(row["temperature_c"]) - previous_temp, 4),
            "service_rule_score": round(rule_score, 4),
        }
        features.append(next_row)
        previous_temperature[asset_id] = float(row["temperature_c"])

    return features


def matrix(rows: list[dict[str, object]], feature_names: list[str] | None = None) -> list[list[float]]:
    names = feature_names or MODEL_FEATURES
    return [[float(row[name]) for name in names] for row in rows]


def labels(rows: list[dict[str, object]], target: str) -> list[int]:
    return [int(row[target]) for row in rows]
