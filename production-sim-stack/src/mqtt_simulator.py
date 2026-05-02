from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = BASE_DIR / "artifacts"


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


def build_messages(limit: int | None = None) -> list[dict[str, object]]:
    messages = []
    for event in pipeline.score_events(pipeline.load_events())[:limit]:
        messages.append(
            {
                "topic": event["mqtt_topic"],
                "payload": {
                    "event_id": event["event_id"],
                    "line": event["line"],
                    "asset_family": event["asset_family"],
                    "timestamp": event["timestamp"],
                    "opcua_node": event["opcua_node"],
                    "predicted_service_escalation_probability": event["predicted_service_escalation_probability"],
                    "predicted_service_escalation": event["predicted_service_escalation"],
                    "simulation_note": "Dry-run simulated MQTT payload; no real broker or industrial integration.",
                    "decision_boundary": "advisory human-review triage only",
                },
            }
        )
    return messages


def write_messages(output_dir: Path = ARTIFACT_DIR, limit: int | None = None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "mqtt_messages.jsonl"
    path.write_text(
        "\n".join(json.dumps(message, sort_keys=True) for message in build_messages(limit=limit)) + "\n",
        encoding="utf-8",
    )
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate simulated MQTT messages for local review.")
    parser.add_argument("--dry-run", action="store_true", help="Print messages instead of writing JSONL.")
    parser.add_argument("--messages", type=int, default=None, help="Limit the number of messages.")
    args = parser.parse_args()

    if args.dry_run:
        for message in build_messages(limit=args.messages):
            print(json.dumps(message, sort_keys=True))
        print("Dry run only: no MQTT broker was contacted.")
        return

    path = write_messages(limit=args.messages)
    print(f"Generated MQTT simulation messages: {path}")


if __name__ == "__main__":
    main()
