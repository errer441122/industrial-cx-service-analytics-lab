from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]


def _load_pipeline_module():
    pipeline_path = BASE_DIR / "src" / "pipeline.py"
    spec = importlib.util.spec_from_file_location("industrial_production_pipeline", pipeline_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load industrial production pipeline.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pipeline = _load_pipeline_module()

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - local tests do not require FastAPI
    FastAPI = None
    BaseModel = object


class ServiceRiskRequest(BaseModel):
    event_id: str
    line: str
    bike_family: str
    timestamp: str
    opcua_node: str
    vibration_rms: float
    temperature_c: float
    battery_voltage: float
    oil_pressure_bar: float
    service_delay_days: int
    nps: int
    warranty_claims: int
    telemetry_dropouts: int
    mqtt_topic: str
    customer_note: str
    service_escalation: int = 0


def score_payload(payload: dict[str, Any]) -> dict[str, Any]:
    probability = pipeline.score_event(payload)
    return {
        "event_id": payload["event_id"],
        "bike_family": payload["bike_family"],
        "predicted_service_escalation_probability": probability,
        "predicted_service_escalation": int(probability >= pipeline.SERVICE_ESCALATION_THRESHOLD),
        "decision_boundary": "advisory human-review triage only",
    }


if FastAPI:
    app = FastAPI(title="Industrial CX Production Simulation API", version="1.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/score/service-risk")
    def score_service_risk(payload: ServiceRiskRequest) -> dict[str, Any]:
        return score_payload(payload.model_dump())
else:
    app = None
