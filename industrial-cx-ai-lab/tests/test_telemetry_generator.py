import importlib.util
import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from telemetry_generator import EXPECTED_FIELDS, generate_telemetry


class TelemetryGeneratorTest(unittest.TestCase):
    def test_generator_returns_expected_fields_and_labels(self):
        rows = generate_telemetry(asset_count=4, periods=48)

        self.assertEqual(len(rows), 192)
        self.assertTrue(set(EXPECTED_FIELDS).issubset(rows[0].keys()))
        self.assertGreater(sum(int(row["anomaly_label"]) for row in rows), 0)
        self.assertGreater(sum(int(row["service_escalation_label"]) for row in rows), 0)
        self.assertLess(sum(int(row["anomaly_label"]) for row in rows), len(rows))


if __name__ == "__main__":
    unittest.main()
