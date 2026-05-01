import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = BASE_DIR / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pipeline = load_module("industrial_prod_pipeline_test", "src/pipeline.py")
orchestrate = load_module("industrial_prod_orchestrate_test", "src/orchestrate.py")
api = load_module("industrial_prod_api_test", "src/api.py")
mqtt_simulator = load_module("industrial_prod_mqtt_test", "src/mqtt_simulator.py")


class IndustrialProductionSimulationStackTest(unittest.TestCase):
    def test_scoring_flags_repeat_fault_context(self):
        events = pipeline.load_events()
        event = next(row for row in events if row["event_id"] == "IE-002")
        self.assertGreaterEqual(pipeline.score_event(event), pipeline.SERVICE_ESCALATION_THRESHOLD)
        self.assertGreaterEqual(pipeline.count_text_risk_hits(str(event["customer_note"])), 4)

    def test_mqtt_messages_preserve_topics(self):
        messages = mqtt_simulator.build_messages()
        self.assertEqual(len(messages), 20)
        self.assertTrue(all("topic" in message and "payload" in message for message in messages))
        self.assertIn("factory/line2/multistrada/service-risk", {message["topic"] for message in messages})

    def test_orchestration_writes_lifecycle_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = orchestrate.run(output_dir=Path(temp_dir))
            self.assertEqual(manifest["rows"], 20)
            self.assertGreaterEqual(manifest["metrics"]["accuracy"], 0.9)
            self.assertGreaterEqual(manifest["metrics"]["f1"], 0.9)

            mlflow_payload = json.loads(Path(manifest["artifacts"]["mlflow"]).read_text(encoding="utf-8"))
            self.assertEqual(mlflow_payload["experiment"], "industrial-cx-production-sim")

            with closing(sqlite3.connect(manifest["artifacts"]["mart"])) as connection:
                count = connection.execute("SELECT COUNT(*) FROM industrial_service_features").fetchone()[0]
            self.assertEqual(count, 20)

    def test_api_scoring_function_is_dependency_light(self):
        payload = pipeline.load_events()[1]
        response = api.score_payload(payload)
        self.assertIn("predicted_service_escalation_probability", response)
        self.assertIn("risk_score", response)
        self.assertEqual(response["decision_boundary"], "advisory human-review triage only")

    def test_api_anomaly_scoring_function_is_dependency_light(self):
        payload = {
            "asset_id": "line-01-pump-01",
            "temperature_c": 91.0,
            "vibration_mm_s": 6.4,
            "pressure_bar": 1.2,
            "service_delay_days": 14,
            "error_code_count": 3,
        }
        response = api.score_anomaly_payload(payload)
        self.assertTrue(response["human_review_required"])
        self.assertEqual(response["model_source"], "local_simulated_rule_baseline")

    def test_fastapi_endpoints_when_available(self):
        if api.app is None:
            self.skipTest("FastAPI is not installed.")
        try:
            from fastapi.testclient import TestClient
        except Exception as exc:  # pragma: no cover - optional dependency path
            self.skipTest(f"FastAPI TestClient unavailable: {exc}")

        client = TestClient(api.app)
        health = client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "ok")

        payload = {
            "asset_id": "line-01-pump-01",
            "temperature_c": 91.0,
            "vibration_mm_s": 6.4,
            "pressure_bar": 1.2,
            "service_delay_days": 14,
            "customer_satisfaction_score": 5.7,
        }
        service = client.post("/score/service-risk", json=payload)
        anomaly = client.post("/score/anomaly", json=payload)
        self.assertEqual(service.status_code, 200)
        self.assertEqual(anomaly.status_code, 200)
        self.assertIn("risk_score", service.json())
        self.assertIn("anomaly_score", anomaly.json())


if __name__ == "__main__":
    unittest.main()
