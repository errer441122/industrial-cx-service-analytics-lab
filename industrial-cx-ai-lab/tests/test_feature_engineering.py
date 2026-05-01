import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from feature_engineering import MODEL_FEATURES, build_feature_table
from telemetry_generator import generate_telemetry


class FeatureEngineeringTest(unittest.TestCase):
    def test_feature_table_adds_model_fields(self):
        rows = generate_telemetry(asset_count=2, periods=36)
        feature_rows = build_feature_table(rows)

        self.assertEqual(len(feature_rows), len(rows))
        for field in MODEL_FEATURES:
            self.assertIn(field, feature_rows[0])
        self.assertTrue(all(0.0 <= float(row["service_rule_score"]) <= 1.0 for row in feature_rows))


if __name__ == "__main__":
    unittest.main()
