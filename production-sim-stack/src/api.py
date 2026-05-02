from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"


def _load_local_module(name: str, filename: str):
    path = SRC_DIR / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


model_adapter = _load_local_module("industrial_model_adapter", "model_adapter.py")

try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover - adapter tests do not require FastAPI
    FastAPI = None


def score_payload(payload: dict[str, Any]) -> dict[str, Any]:
    response = model_adapter.score_service_risk_payload(payload)
    probability = response["risk_score"]
    return {
        **response,
        "event_id": payload.get("event_id", response["asset_id"]),
        "asset_family": payload.get("asset_family", "synthetic-industrial-asset"),
        "predicted_service_escalation_probability": probability,
        "predicted_service_escalation": int(probability >= 0.45),
        "decision_boundary": "advisory human-review triage only",
    }


def score_anomaly_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return model_adapter.score_anomaly_payload(payload)


if FastAPI:
    app = FastAPI(title="Industrial CX Production Simulation API", version="2.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {
            "status": "ok",
            "mode": "local_simulation",
            "disclaimer": model_adapter.DISCLAIMER,
        }

    @app.post("/score/service-risk")
    def score_service_risk(payload: dict[str, Any]) -> dict[str, Any]:
        return score_payload(payload)

    @app.post("/score/anomaly")
    def score_anomaly(payload: dict[str, Any]) -> dict[str, Any]:
        return score_anomaly_payload(payload)
else:
    app = None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="FastAPI-compatible local scoring module for the industrial CX simulation."
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Print an example score response without starting an API server.",
    )
    args = parser.parse_args()
    if args.example:
        payload = {
            "asset_id": "line-01-pump-01",
            "temperature_c": 82.5,
            "vibration_mm_s": 6.2,
            "pressure_bar": 1.1,
            "operating_hours": 1250,
            "service_delay_days": 14,
            "customer_satisfaction_score": 5.8,
        }
        print(json.dumps(score_payload(payload), indent=2, sort_keys=True))
    else:
        print("Import this module with FastAPI/uvicorn, or run with --example for a local score.")


if __name__ == "__main__":
    main()
