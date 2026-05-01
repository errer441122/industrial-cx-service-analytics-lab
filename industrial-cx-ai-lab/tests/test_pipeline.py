import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


PIPELINE_PATH = Path(__file__).resolve().parents[1] / "src" / "run_pipeline.py"
SPEC = importlib.util.spec_from_file_location("industrial_cx_pipeline", PIPELINE_PATH)
pipeline = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = pipeline
SPEC.loader.exec_module(pipeline)


class IndustrialCxPipelineTest(unittest.TestCase):
    def test_text_mining_flags_service_risk_terms(self):
        text = "repeat vibration complaint unresolved dealer delay"
        self.assertGreaterEqual(pipeline.count_text_risk_hits(text), 5)

    def test_pipeline_generates_industrial_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = pipeline.run_pipeline(output_dir=Path(temp_dir))

            self.assertEqual(result["rows"], 28)
            self.assertGreaterEqual(result["metrics"]["accuracy"], 0.85)
            self.assertGreaterEqual(result["metrics"]["f1"], 0.85)
            self.assertTrue(Path(result["artifacts"]["model_card"]).exists())
            self.assertTrue(Path(result["artifacts"]["influx"]).exists())

            with closing(sqlite3.connect(result["mart"])) as connection:
                row_count = connection.execute(
                    "SELECT COUNT(*) FROM industrial_cx_features"
                ).fetchone()[0]
                review_count = connection.execute(
                    """
                    SELECT COUNT(*)
                    FROM industrial_cx_features
                    WHERE predicted_churn_probability >= 0.5
                    """
                ).fetchone()[0]

            self.assertEqual(row_count, 28)
            self.assertGreaterEqual(review_count, 10)


if __name__ == "__main__":
    unittest.main()
