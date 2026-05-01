from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from anomaly_detection import run_anomaly_detection
from evaluate import (
    write_feature_importance,
    write_influx_line_protocol,
    write_json,
    write_policy_note,
)
from feature_engineering import build_feature_table, load_telemetry
from service_risk_model import run_service_risk_model
from telemetry_generator import generate_telemetry, write_service_events, write_telemetry_csv


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
ARTIFACT_DIR = BASE_DIR / "artifacts"


def run_pipeline(
    output_dir: Path = ARTIFACT_DIR,
    data_dir: Path = DATA_DIR,
    asset_count: int = 4,
    periods: int = 96,
    partition: int | None = None,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    generated_rows = generate_telemetry(asset_count=asset_count, periods=periods)
    telemetry_path = write_telemetry_csv(generated_rows, data_dir / "simulated_telemetry.csv")
    service_events_path = write_service_events(
        generated_rows,
        data_dir / "simulated_service_events.csv",
    )

    loaded_rows = load_telemetry(telemetry_path)
    feature_rows = build_feature_table(loaded_rows)
    anomaly_metrics = run_anomaly_detection(feature_rows)
    service_metrics = run_service_risk_model(feature_rows)

    anomaly_path = write_json(anomaly_metrics, output_dir / "anomaly_metrics.json")
    service_path = write_json(service_metrics, output_dir / "service_risk_metrics.json")
    feature_path = write_feature_importance(
        service_metrics["feature_importance"],
        output_dir / "feature_importance.csv",
    )
    policy_path = write_policy_note(
        anomaly_metrics,
        service_metrics,
        output_dir / "maintenance_policy_note.md",
    )
    influx_path = write_influx_line_protocol(
        feature_rows,
        output_dir / "influx_line_protocol.txt",
    )

    # Backward-compatible aliases for earlier reviewer links in this repository.
    write_json(service_metrics, output_dir / "metrics.json")
    write_json(
        {
            "model_name": "industrial_service_risk_random_forest_baseline",
            "target": "service_escalation_label",
            "metrics": service_metrics["metrics"],
            "intended_use": "Human-reviewed service triage simulation.",
            "out_of_scope": [
                "warranty automation",
                "safety decision automation",
                "customer treatment automation",
                "production industrial control",
            ],
            "limitations": [
                "synthetic data only",
                "controlled anomaly labels",
                "local CPU execution only",
                "no real Ducati, OPC UA, MQTT, Influx, Grafana, Slurm, cloud, or edge integration",
            ],
        },
        output_dir / "model_card.json",
    )
    (output_dir / "service_risk_influx.lp").write_text(
        influx_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": len(feature_rows),
        "assets": asset_count,
        "periods_per_asset": periods,
        "partition": partition,
        "data": {
            "simulated_telemetry": str(telemetry_path),
            "simulated_service_events": str(service_events_path),
        },
        "artifacts": {
            "anomaly_metrics": str(anomaly_path),
            "service_risk_metrics": str(service_path),
            "feature_importance": str(feature_path),
            "maintenance_policy_note": str(policy_path),
            "influx_line_protocol": str(influx_path),
        },
        "disclaimer": (
            "Synthetic local-only industrial analytics simulation; no real Ducati, "
            "customer, dealer, plant, telemetry, OPC UA, MQTT, Influx, Grafana, "
            "Slurm, cloud, or edge execution."
        ),
    }
    manifest_path = write_json(manifest, output_dir / "run_manifest.json")
    manifest["manifest"] = str(manifest_path)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the simulated industrial CX AI lab.")
    parser.add_argument("--assets", type=int, default=4, help="Number of synthetic assets.")
    parser.add_argument("--periods", type=int, default=96, help="Telemetry periods per asset.")
    parser.add_argument(
        "--partition",
        type=int,
        default=None,
        help="Optional Slurm-style partition id recorded in the manifest.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_pipeline(asset_count=args.assets, periods=args.periods, partition=args.partition)
    service = json.loads(Path(result["artifacts"]["service_risk_metrics"]).read_text(encoding="utf-8"))
    anomaly = json.loads(Path(result["artifacts"]["anomaly_metrics"]).read_text(encoding="utf-8"))
    print(
        "Industrial CX AI lab completed: "
        f"rows={result['rows']} "
        f"service_f1={service['f1']} "
        f"anomaly_rule_f1={anomaly['rule_based']['f1']}"
    )


if __name__ == "__main__":
    main()
