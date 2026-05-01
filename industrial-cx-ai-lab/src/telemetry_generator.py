from __future__ import annotations

import csv
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Iterable


EXPECTED_FIELDS = [
    "timestamp",
    "asset_id",
    "rpm",
    "temperature_c",
    "vibration_mm_s",
    "pressure_bar",
    "torque_nm",
    "operating_hours",
    "error_code_count",
    "service_delay_days",
    "customer_satisfaction_score",
    "anomaly_label",
    "service_escalation_label",
]

ASSET_IDS = [
    "line-01-pump-01",
    "line-01-compressor-02",
    "line-02-pump-01",
    "line-02-testbench-01",
]


def _clamp(value: float, lower: float, upper: float) -> float:
    return min(max(value, lower), upper)


def generate_telemetry(
    asset_count: int = 4,
    periods: int = 96,
    start: datetime | None = None,
    interval_minutes: int = 15,
) -> list[dict[str, object]]:
    """Build deterministic simulated industrial-service telemetry.

    The signals are synthetic and designed only for local analytics tests. They
    are not Ducati, dealer, plant, equipment, or production telemetry.
    """

    if asset_count < 1:
        raise ValueError("asset_count must be at least 1")
    if periods < 24:
        raise ValueError("periods must be at least 24")

    start_time = start or datetime(2026, 4, 1, 8, 0, tzinfo=timezone.utc)
    rows: list[dict[str, object]] = []
    assets = ASSET_IDS[:asset_count]

    for asset_index, asset_id in enumerate(assets):
        base_hours = 620.0 + asset_index * 140.0
        for period in range(periods):
            ts = start_time + timedelta(minutes=interval_minutes * period)
            phase = period / 6.0 + asset_index * 0.8

            rpm = 2600 + 280 * math.sin(phase) + asset_index * 55
            temperature = 72.0 + 4.5 * math.sin(phase / 1.7) + asset_index * 1.2
            vibration = 2.4 + 0.35 * math.sin(phase * 1.4) + asset_index * 0.18
            pressure = 2.9 + 0.16 * math.cos(phase / 1.3) - asset_index * 0.05
            torque = 105.0 + 10.5 * math.sin(phase / 2.0) + asset_index * 3.0
            operating_hours = base_hours + period * (interval_minutes / 60.0)
            error_count = 0
            service_delay = max(0, (period // 24) + asset_index - 1)
            satisfaction = 8.6 - asset_index * 0.25 - service_delay * 0.08
            anomaly_label = 0

            # Controlled anomaly families: temperature spike, vibration drift,
            # pressure drop, error burst, and delayed maintenance.
            if 20 + asset_index * 2 <= period <= 25 + asset_index * 2:
                temperature += 17.5 + asset_index
                error_count += 1
                satisfaction -= 0.7
                anomaly_label = 1

            if asset_index % 2 == 1 and 44 <= period <= 58:
                vibration += 0.22 * (period - 43)
                satisfaction -= 0.05 * (period - 43)
                anomaly_label = 1

            if asset_index == 2 and 60 <= period <= 68:
                pressure -= 1.05
                torque -= 15.0
                error_count += 1
                anomaly_label = 1

            if asset_index == 3 and 70 <= period <= 76:
                error_count += 4
                service_delay += 5
                satisfaction -= 1.2
                anomaly_label = 1

            if asset_index == 0 and 82 <= period <= 89:
                service_delay += 13
                temperature += 5.0
                vibration += 1.4
                satisfaction -= 2.0
                anomaly_label = 1

            satisfaction = _clamp(satisfaction, 1.0, 10.0)
            service_escalation = int(
                error_count >= 3
                or service_delay >= 10
                or (anomaly_label == 1 and satisfaction <= 7.1)
                or (vibration >= 5.2 and pressure <= 2.1)
            )

            rows.append(
                {
                    "timestamp": ts.isoformat().replace("+00:00", "Z"),
                    "asset_id": asset_id,
                    "rpm": round(rpm, 2),
                    "temperature_c": round(temperature, 2),
                    "vibration_mm_s": round(vibration, 3),
                    "pressure_bar": round(max(0.4, pressure), 3),
                    "torque_nm": round(torque, 2),
                    "operating_hours": round(operating_hours, 2),
                    "error_code_count": int(error_count),
                    "service_delay_days": int(service_delay),
                    "customer_satisfaction_score": round(satisfaction, 2),
                    "anomaly_label": int(anomaly_label),
                    "service_escalation_label": int(service_escalation),
                }
            )

    return rows


def write_telemetry_csv(rows: Iterable[dict[str, object]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPECTED_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in EXPECTED_FIELDS})
    return path


def write_service_events(rows: list[dict[str, object]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_asset: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_asset.setdefault(str(row["asset_id"]), []).append(row)

    fields = [
        "asset_id",
        "telemetry_rows",
        "anomaly_count",
        "service_escalation_count",
        "max_service_delay_days",
        "avg_customer_satisfaction_score",
        "simulation_note",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for asset_id, asset_rows in sorted(by_asset.items()):
            writer.writerow(
                {
                    "asset_id": asset_id,
                    "telemetry_rows": len(asset_rows),
                    "anomaly_count": sum(int(row["anomaly_label"]) for row in asset_rows),
                    "service_escalation_count": sum(
                        int(row["service_escalation_label"]) for row in asset_rows
                    ),
                    "max_service_delay_days": max(
                        int(row["service_delay_days"]) for row in asset_rows
                    ),
                    "avg_customer_satisfaction_score": round(
                        mean(float(row["customer_satisfaction_score"]) for row in asset_rows),
                        3,
                    ),
                    "simulation_note": "Synthetic service summary; no real Ducati data.",
                }
            )
    return path
