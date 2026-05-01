from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


LAB_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = LAB_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validate_cx_data = load_module("validate_cx_data_test", SRC_DIR / "validate_cx_data.py")
build_cx_summary = load_module("build_cx_summary_test", SRC_DIR / "build_cx_summary.py")


class CxMetricsTest(unittest.TestCase):
    def test_sample_data_passes_validation(self):
        errors = validate_cx_data.validate_file()
        self.assertEqual(errors, [])

    def test_core_customer_satisfaction_metrics(self):
        rows = validate_cx_data.load_rows()
        summary = build_cx_summary.build_summary(rows)

        self.assertEqual(summary["records"], 12)
        self.assertEqual(summary["weighted_feedback_volume"], 1055)
        self.assertEqual(summary["customer_satisfaction_rate_pct"], 65.9)
        self.assertEqual(summary["at_risk_segment_count"], 1)
        self.assertEqual(summary["at_risk_segments"], ["First-Time Owners"])
        self.assertEqual(summary["journey_friction_index"], 2.44)
        self.assertEqual(summary["follow_up_completion_rate_pct"], 71.4)
        self.assertEqual(summary["post_action_improvement_delta"], 1.0)

    def test_monthly_trend_is_available_for_bi_reporting(self):
        rows = validate_cx_data.load_rows()
        summary = build_cx_summary.build_summary(rows)
        trend = summary["monthly_trend"]

        self.assertEqual(set(trend), {"2026-01", "2026-02", "2026-03", "2026-04"})
        self.assertGreater(trend["2026-03"]["feedback_volume"], trend["2026-04"]["feedback_volume"])


if __name__ == "__main__":
    unittest.main()
