from __future__ import annotations

from typing import Any


DISCLAIMER = "Simulation only; not a production industrial decision system."


def _value(payload: dict[str, Any], *names: str, default: float = 0.0) -> float:
    for name in names:
        if name in payload and payload[name] is not None:
            try:
                return float(payload[name])
            except (TypeError, ValueError):
                return default
    return default


def _band(score: float) -> str:
    if score >= 0.72:
        return "high"
    if score >= 0.45:
        return "medium"
    return "low"


def score_anomaly_payload(payload: dict[str, Any]) -> dict[str, Any]:
    temperature = _value(payload, "temperature_c", default=72.0)
    vibration = _value(payload, "vibration_mm_s", "vibration_rms", default=2.4)
    pressure = _value(payload, "pressure_bar", "oil_pressure_bar", default=2.8)
    errors = _value(payload, "error_code_count", "telemetry_dropouts", default=0.0)
    service_delay = _value(payload, "service_delay_days", default=0.0)

    score = min(
        1.0,
        0.28 * max(0.0, (temperature - 82.0) / 22.0)
        + 0.28 * max(0.0, (vibration - 3.0) / 4.0)
        + 0.18 * max(0.0, (2.4 - pressure) / 1.4)
        + 0.14 * min(1.0, errors / 4.0)
        + 0.12 * min(1.0, service_delay / 18.0),
    )

    return {
        "asset_id": str(payload.get("asset_id") or payload.get("event_id") or "unknown"),
        "anomaly_score": round(score, 4),
        "anomaly_band": _band(score),
        "predicted_anomaly": bool(score >= 0.5),
        "human_review_required": bool(score >= 0.5),
        "model_source": "local_simulated_rule_baseline",
        "disclaimer": DISCLAIMER,
    }


def score_service_risk_payload(payload: dict[str, Any]) -> dict[str, Any]:
    anomaly = score_anomaly_payload(payload)
    service_delay = _value(payload, "service_delay_days", default=0.0)
    satisfaction = _value(
        payload,
        "customer_satisfaction_score",
        "nps",
        default=7.5,
    )
    if "nps" in payload and "customer_satisfaction_score" not in payload:
        satisfaction = max(1.0, min(10.0, (satisfaction + 2.0) / 1.2))
    warranty_claims = _value(payload, "warranty_claims", default=0.0)
    errors = _value(payload, "error_code_count", "telemetry_dropouts", default=0.0)

    score = min(
        1.0,
        0.38 * float(anomaly["anomaly_score"])
        + 0.22 * min(1.0, service_delay / 18.0)
        + 0.18 * max(0.0, (8.0 - satisfaction) / 7.0)
        + 0.12 * min(1.0, warranty_claims / 3.0)
        + 0.10 * min(1.0, errors / 4.0),
    )
    risk_band = _band(score)

    return {
        "asset_id": anomaly["asset_id"],
        "risk_score": round(score, 4),
        "risk_band": risk_band,
        "human_review_required": bool(score >= 0.45),
        "model_source": "local_simulated_baseline",
        "disclaimer": DISCLAIMER,
    }
