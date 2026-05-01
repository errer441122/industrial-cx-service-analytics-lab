import json
import sys
import tempfile
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from anomaly_detection import run_anomaly_detection
from feature_engineering import build_feature_table
from run_pipeline import run_pipeline
from telemetry_generator import generate_telemetry


class AnomalyPipelineTest(unittest.TestCase):
    def test_anomaly_detection_reports_rule_and_isolation_paths(self):
        rows = build_feature_table(generate_telemetry(asset_count=4, periods=48))
        report = run_anomaly_detection(rows)

        self.assertIn("rule_based", report)
        self.assertIn("isolation_forest", report)
        self.assertGreaterEqual(report["rule_based"]["f1"], 0.4)

    def test_pipeline_writes_required_artifacts(self):
        with tempfile.TemporaryDirectory() as output_dir, tempfile.TemporaryDirectory() as data_dir:
            manifest = run_pipeline(
                output_dir=Path(output_dir),
                data_dir=Path(data_dir),
                asset_count=4,
                periods=48,
            )

            expected = [
                "anomaly_metrics",
                "service_risk_metrics",
                "feature_importance",
                "maintenance_policy_note",
                "influx_line_protocol",
            ]
            for key in expected:
                self.assertTrue(Path(manifest["artifacts"][key]).exists())

            service = json.loads(Path(manifest["artifacts"]["service_risk_metrics"]).read_text())
            self.assertIn("roc_auc", service)
            self.assertIn("pr_auc", service)


if __name__ == "__main__":
    unittest.main()
