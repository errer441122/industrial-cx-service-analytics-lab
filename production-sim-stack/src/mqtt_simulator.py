from __future__ import annotations

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


def build_messages() -> list[dict[str, object]]:
    messages = []
    for event in pipeline.score_events(pipeline.load_events()):
        messages.append(
            {
                "topic": event["mqtt_topic"],
                "payload": {
                    "event_id": event["event_id"],
                    "line": event["line"],
                    "bike_family": event["bike_family"],
                    "timestamp": event["timestamp"],
                    "opcua_node": event["opcua_node"],
                    "predicted_service_escalation_probability": event["predicted_service_escalation_probability"],
                    "predicted_service_escalation": event["predicted_service_escalation"],
                    "decision_boundary": "advisory human-review triage only",
                },
            }
        )
    return messages


def write_messages(output_dir: Path = ARTIFACT_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "mqtt_messages.jsonl"
    path.write_text(
        "\n".join(json.dumps(message, sort_keys=True) for message in build_messages()) + "\n",
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_messages()
    print(f"Generated MQTT simulation messages: {path}")


if __name__ == "__main__":
    main()
