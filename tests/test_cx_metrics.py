"""Behavioral CX tests on the REAL Olist dataset.

Assert methodological correctness and consistency, plus one robust real
fact (late delivery strongly reduces satisfaction) — not hand-coded
constants.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = LAB_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SRC_DIR / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


validate_cx_data = load("validate_cx_data")
cx_driver_analysis = load("cx_driver_analysis")
build_cx_summary = load("build_cx_summary")


class CxRealDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = cx_driver_analysis.load_reviews()
        cls.result = cx_driver_analysis.run(cls.rows)
        cls.summary = build_cx_summary.build_summary(cls.rows)

    def test_real_data_validates_and_is_substantial(self):
        self.assertEqual(validate_cx_data.validate_file(), [])
        self.assertGreater(len(self.rows), 1000)
        self.assertIn("real", self.result["dataset"].lower())

    def test_core_rates_are_plausible(self):
        s = self.summary
        self.assertTrue(0.0 < s["customer_satisfaction_rate"] < 1.0)
        self.assertTrue(1.0 <= s["avg_review_score"] <= 5.0)
        self.assertTrue(0.0 <= s["late_delivery_rate"] <= 1.0)
        self.assertTrue(-100.0 <= s["nps_proxy"] <= 100.0)

    def test_driver_table_has_inference_and_is_ranked(self):
        drivers = self.result["drivers"]
        self.assertGreater(len(drivers), 5)
        expected = {"dimension", "level", "n", "satisfied_rate", "diff_vs_rest",
                    "diff_ci", "z", "p_value", "cohens_h", "effect", "significant"}
        for d in drivers:
            self.assertTrue(expected.issubset(d))
            self.assertGreaterEqual(d["n"], cx_driver_analysis.MIN_GROUP)
        mags = [abs(d["cohens_h"]) for d in drivers]
        self.assertEqual(mags, sorted(mags, reverse=True))

    def test_nps_is_well_formed(self):
        ov = self.result["nps"]["overall"]
        self.assertLessEqual(ov["promoters"] + ov["detractors"], ov["n"])
        self.assertTrue(-100.0 <= ov["nps"] <= 100.0)
        self.assertLessEqual(ov["nps_ci_95"][0], ov["nps"])
        self.assertGreaterEqual(ov["nps_ci_95"][1], ov["nps"])

    def test_late_delivery_hurts_satisfaction(self):
        coh = self.result["delivery_sla_cohort"]
        self.assertGreater(coh["on_time_satisfied_rate"], coh["late_satisfied_rate"])
        self.assertTrue(coh["significant"])
        self.assertGreater(coh["on_time_mean_score"], coh["late_mean_score"])

    def test_multivariate_controls_and_late_is_negative(self):
        mv = self.result["multivariate_drivers"]
        names = {c["feature"] for c in mv["coefficients"]}
        self.assertIn("intercept", names)
        self.assertIn("late_delivery", names)
        late = next(c for c in mv["coefficients"] if c["feature"] == "late_delivery")
        self.assertLess(late["odds_ratio"], 1.0)
        self.assertTrue(late["significant"])

    def test_comment_themes_extracted(self):
        themes = self.result["comment_themes"]
        self.assertTrue(themes)
        for t in themes:
            self.assertTrue(0.0 <= t["share_of_comments"] <= 1.0)
            self.assertTrue(1.0 <= t["avg_review_score"] <= 5.0)

    def test_monthly_trend_available_and_sorted(self):
        trend = self.summary["monthly_trend"]
        self.assertGreaterEqual(len(trend), 6)
        self.assertEqual(list(trend), sorted(trend))


if __name__ == "__main__":
    unittest.main()
