from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "industrial-cx-ai-lab" / "src"
ARTIFACT_DIR = REPO_ROOT / "benchmarks" / "artifacts"


def _load(name: str, filename: str):
    path = SRC_DIR / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SRC_DIR))
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


telemetry_generator = _load("bench_telemetry_generator", "telemetry_generator.py")
feature_engineering = _load("bench_feature_engineering", "feature_engineering.py")
anomaly_detection = _load("bench_anomaly_detection", "anomaly_detection.py")
service_risk_model = _load("bench_service_risk_model", "service_risk_model.py")


def run_benchmark(quick: bool = False) -> dict[str, object]:
    asset_count = 4
    periods = 48 if quick else 240

    start = time.perf_counter()
    rows = telemetry_generator.generate_telemetry(asset_count=asset_count, periods=periods)
    generated_seconds = time.perf_counter() - start

    start = time.perf_counter()
    feature_rows = feature_engineering.build_feature_table(rows)
    feature_seconds = time.perf_counter() - start

    start = time.perf_counter()
    anomaly_report = anomaly_detection.run_anomaly_detection(feature_rows)
    service_report = service_risk_model.run_service_risk_model(feature_rows)
    scoring_seconds = time.perf_counter() - start

    total_scoring_time = feature_seconds + scoring_seconds
    rows_per_second = len(rows) / total_scoring_time if total_scoring_time else 0.0

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": "quick" if quick else "standard",
        "rows": len(rows),
        "asset_count": asset_count,
        "periods_per_asset": periods,
        "timing_seconds": {
            "telemetry_generation": round(generated_seconds, 6),
            "feature_engineering": round(feature_seconds, 6),
            "anomaly_and_service_scoring": round(scoring_seconds, 6),
            "feature_plus_scoring": round(total_scoring_time, 6),
        },
        "rows_per_second_feature_plus_scoring": round(rows_per_second, 2),
        "metrics": {
            "anomaly_rule_f1": anomaly_report["rule_based"]["f1"],
            "anomaly_isolation_forest_f1": anomaly_report["isolation_forest"]["f1"],
            "service_risk_f1": service_report["f1"],
            "service_risk_roc_auc": service_report["roc_auc"],
        },
        "hardware_note": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
        },
        "disclaimer": (
            "Local CPU benchmark only. Not executed on a real BI-REX, CINECA, "
            "IT4LIA, Ducati, Slurm, cloud, GPU, or edge environment."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark local industrial scoring.")
    parser.add_argument("--quick", action="store_true", help="Use a small CPU-only dataset.")
    args = parser.parse_args()

    result = run_benchmark(quick=args.quick)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    path = ARTIFACT_DIR / "local_cpu_benchmark.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(
        "Industrial scoring benchmark completed: "
        f"rows={result['rows']} "
        f"rows_per_second={result['rows_per_second_feature_plus_scoring']} "
        f"artifact={path}"
    )


if __name__ == "__main__":
    main()
