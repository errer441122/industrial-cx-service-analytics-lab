from __future__ import annotations

import csv
import importlib.util
import json
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = BASE_DIR / "artifacts"


def _load_module(name: str, relative_path: str):
    path = BASE_DIR / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {relative_path}.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pipeline = _load_module("industrial_production_pipeline", "src/pipeline.py")
mqtt_simulator = _load_module("industrial_mqtt_simulator", "src/mqtt_simulator.py")


def write_predictions(scored: list[dict[str, object]], output_dir: Path) -> Path:
    path = output_dir / "service_escalation_predictions.csv"
    fields = [
        "event_id",
        "line",
        "bike_family",
        "predicted_service_escalation_probability",
        "predicted_service_escalation",
        "service_escalation",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in scored:
            writer.writerow({field: row[field] for field in fields})
    return path


def write_sqlite_mart(scored: list[dict[str, object]], output_dir: Path) -> Path:
    path = output_dir / "industrial_service_feature_mart.sqlite"
    if path.exists():
        path.unlink()
    with closing(sqlite3.connect(path)) as connection:
        connection.execute(
            """
            CREATE TABLE industrial_service_features (
                event_id TEXT PRIMARY KEY,
                line TEXT NOT NULL,
                bike_family TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                opcua_node TEXT NOT NULL,
                vibration_rms REAL NOT NULL,
                temperature_c REAL NOT NULL,
                battery_voltage REAL NOT NULL,
                oil_pressure_bar REAL NOT NULL,
                service_delay_days INTEGER NOT NULL,
                nps INTEGER NOT NULL,
                warranty_claims INTEGER NOT NULL,
                telemetry_dropouts INTEGER NOT NULL,
                text_risk_hits INTEGER NOT NULL,
                predicted_service_escalation_probability REAL NOT NULL,
                service_escalation INTEGER NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO industrial_service_features VALUES (
                :event_id,
                :line,
                :bike_family,
                :timestamp,
                :opcua_node,
                :vibration_rms,
                :temperature_c,
                :battery_voltage,
                :oil_pressure_bar,
                :service_delay_days,
                :nps,
                :warranty_claims,
                :telemetry_dropouts,
                :text_risk_hits,
                :predicted_service_escalation_probability,
                :service_escalation
            )
            """,
            scored,
        )
        connection.commit()
    return path


def write_influx(scored: list[dict[str, object]], output_dir: Path) -> Path:
    path = output_dir / "industrial_service_influx.lp"
    lines = []
    for index, row in enumerate(scored):
        timestamp_ns = 1_741_158_000_000_000_000 + index * 60_000_000_000
        tags = f"line={row['line']},bike_family={row['bike_family']}"
        fields = (
            f"risk_probability={row['predicted_service_escalation_probability']},"
            f"text_risk_hits={row['text_risk_hits']}i,"
            f"telemetry_dropouts={row['telemetry_dropouts']}i"
        )
        lines.append(f"industrial_service_risk,{tags} {fields} {timestamp_ns}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_lifecycle(metrics: dict[str, float], output_dir: Path) -> dict[str, Path]:
    run_id = datetime.now(timezone.utc).strftime("industrial-%Y%m%d%H%M%S")
    mlflow_path = output_dir / "mlflow_run.json"
    mlflow_path.write_text(
        json.dumps(
            {
                "experiment": "industrial-cx-production-sim",
                "run_id": run_id,
                "tracking_uri": "http://localhost:5001",
                "params": {
                    "model_type": "transparent_industrial_risk_baseline",
                    "threshold": pipeline.SERVICE_ESCALATION_THRESHOLD,
                    "source": "simulated_opcua_mqtt_stream",
                },
                "metrics": metrics,
                "artifacts": [
                    "service_escalation_predictions.csv",
                    "industrial_service_feature_mart.sqlite",
                    "industrial_service_influx.lp",
                    "mqtt_messages.jsonl",
                    "model_card.json",
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    minio_path = output_dir / "minio_manifest.json"
    minio_path.write_text(
        json.dumps(
            {
                "endpoint": "http://localhost:9010",
                "bucket": "industrial-cx-artifacts",
                "objects": [
                    "s3://industrial-cx-artifacts/service/model_card.json",
                    "s3://industrial-cx-artifacts/service/predictions.csv",
                    "s3://industrial-cx-artifacts/service/mqtt_messages.jsonl",
                ],
                "note": "Manifest only. Upload requires the docker-compose stack and credentials.",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    model_card_path = output_dir / "model_card.json"
    model_card_path.write_text(
        json.dumps(
            {
                "model_name": "industrial_service_escalation_baseline",
                "model_type": "transparent weighted baseline",
                "threshold": pipeline.SERVICE_ESCALATION_THRESHOLD,
                "intended_use": "Human-reviewed service triage and monitoring",
                "not_for": ["warranty automation", "safety decision automation", "customer treatment automation"],
                "metrics": metrics,
                "limitations": [
                    "simulated data only",
                    "no real OPC UA server",
                    "no real MQTT broker required for CI",
                    "no production plant integration",
                    "no safety certification",
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return {"mlflow": mlflow_path, "minio": minio_path, "model_card": model_card_path}


def run(output_dir: Path = ARTIFACT_DIR) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    scored = pipeline.score_events(pipeline.load_events())
    metrics = pipeline.evaluate(scored)
    predictions_path = write_predictions(scored, output_dir)
    mart_path = write_sqlite_mart(scored, output_dir)
    influx_path = write_influx(scored, output_dir)
    mqtt_path = mqtt_simulator.write_messages(output_dir)
    lifecycle = write_lifecycle(metrics, output_dir)

    manifest_path = output_dir / "run_manifest.json"
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": len(scored),
        "metrics": metrics,
        "artifacts": {
            "predictions": str(predictions_path),
            "mart": str(mart_path),
            "influx": str(influx_path),
            "mqtt": str(mqtt_path),
            **{key: str(value) for key, value in lifecycle.items()},
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def main() -> None:
    manifest = run()
    metrics = manifest["metrics"]
    print(
        "Industrial production simulation completed: "
        f"rows={manifest['rows']} "
        f"accuracy={metrics['accuracy']} "
        f"f1={metrics['f1']}"
    )


if __name__ == "__main__":
    main()
