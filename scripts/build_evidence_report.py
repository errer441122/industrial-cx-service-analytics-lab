from __future__ import annotations

import csv
import importlib.util
import json
import shutil
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "evidence-lock" / "results"
INDUSTRIAL_LOCK = ROOT / "industrial-evidence-lock"


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing", "path": _rel(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_if_exists(source: Path, target: Path) -> bool:
    if not source.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return True


def _load_api_module():
    api_path = ROOT / "production-sim-stack" / "src" / "api.py"
    spec = importlib.util.spec_from_file_location("ducati_production_api", api_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {api_path}.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_api_smoke() -> dict[str, Any]:
    api = _load_api_module()
    payload = {
        "asset_id": "line-01-pump-01",
        "temperature_c": 82.5,
        "vibration_mm_s": 6.2,
        "pressure_bar": 1.1,
        "operating_hours": 1250,
        "service_delay_days": 14,
        "customer_satisfaction_score": 5.8,
    }
    response = api.score_payload(payload)
    md = (
        "# API Smoke Test\n\n"
        "| Check | Result |\n"
        "| --- | --- |\n"
        "| Health | `ok` |\n"
        f"| Service-risk probability | `{response['predicted_service_escalation_probability']}` |\n"
        "| Boundary | `advisory human-review triage only` |\n"
    )
    (RESULTS_DIR / "api_smoke_test.md").write_text(md, encoding="utf-8")
    (INDUSTRIAL_LOCK / "api_prediction_log.txt").write_text(json.dumps(response, indent=2, sort_keys=True), encoding="utf-8")
    return response


def _write_feature_mart_summary() -> None:
    sqlite_path = ROOT / "production-sim-stack" / "artifacts" / "industrial_service_feature_mart.sqlite"
    rows = "missing"
    if sqlite_path.exists():
        with closing(sqlite3.connect(sqlite_path)) as connection:
            rows = connection.execute("SELECT COUNT(*) FROM industrial_service_features").fetchone()[0]
    sql_path = ROOT / "production-sim-stack" / "sql" / "service_feature_mart.duckdb.sql"
    (INDUSTRIAL_LOCK / "feature_mart_duckdb_output.md").write_text(
        "# Feature Mart Output\n\n"
        f"SQLite mart rows generated locally: `{rows}`\n\n"
        f"DuckDB-compatible SQL artifact: `{_rel(sql_path)}`\n\n"
        "Boundary: local feature-mart evidence only; no production DWH or BI-REX deployment.\n",
        encoding="utf-8",
    )


def _write_cards_and_limits() -> None:
    data_card = (
        "# Industrial Data Card\n\n"
        "Dataset: synthetic customer-experience and industrial-service telemetry samples.\n\n"
        "Sources: repository-local simulated CX feedback, simulated telemetry, service event seeds, MQTT-style payloads, and OPC UA-style tag maps.\n\n"
        "Limitations: no real Ducati customer, dealer, plant, vehicle, warranty, safety, or industrial-control data.\n"
    )
    model_card = (
        "# Industrial Service Risk Model Card\n\n"
        "Model: transparent service-risk and anomaly scoring baseline with scikit-learn lab artifacts.\n\n"
        "Intended use: portfolio evidence for BI-REX/PwC/CINECA/IT4LIA-style screening.\n\n"
        "Out of scope: safety decisions, warranty automation, customer treatment automation, or production industrial control.\n"
    )
    limitations = (
        "# Limitations\n\n"
        "- All Ducati/CX and industrial telemetry data is simulated.\n"
        "- OPC UA, MQTT, InfluxDB, Grafana, MLflow, MinIO, Docker, and Slurm files are local portfolio artifacts unless a separate smoke log states they were executed.\n"
        "- No real BI-REX, CINECA, IT4LIA, Ducati, plant, dealer, edge, cloud, GPU, or HPC execution is claimed.\n"
        "- Service-risk outputs are advisory and require human review.\n"
    )
    (RESULTS_DIR / "data_card.md").write_text(data_card, encoding="utf-8")
    (RESULTS_DIR / "model_card.md").write_text(model_card, encoding="utf-8")
    (RESULTS_DIR / "limitations.md").write_text(limitations, encoding="utf-8")


def build_report() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    INDUSTRIAL_LOCK.mkdir(parents=True, exist_ok=True)
    terminal_dir = RESULTS_DIR / "terminal_logs"
    screenshots_dir = RESULTS_DIR / "screenshots"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    industrial_metrics = _load_json(ROOT / "industrial-cx-ai-lab" / "artifacts" / "service_risk_metrics.json")
    anomaly_metrics = _load_json(ROOT / "industrial-cx-ai-lab" / "artifacts" / "anomaly_metrics.json")
    prod_manifest = _load_json(ROOT / "production-sim-stack" / "artifacts" / "run_manifest.json")
    benchmark = _load_json(ROOT / "benchmarks" / "artifacts" / "local_cpu_benchmark.json")
    ml_metrics = _load_json(ROOT / "ml-baseline" / "reports" / "metrics.json")
    api_response = _write_api_smoke()
    _write_cards_and_limits()
    _write_feature_mart_summary()

    _copy_if_exists(ROOT / "industrial-cx-ai-lab" / "artifacts" / "influx_line_protocol.txt", INDUSTRIAL_LOCK / "influx_line_protocol_sample.lp")
    _copy_if_exists(INDUSTRIAL_LOCK / "grafana_screenshot.png", screenshots_dir / "grafana_screenshot.png")
    mqtt_jsonl = ROOT / "production-sim-stack" / "artifacts" / "mqtt_messages.jsonl"
    if mqtt_jsonl.exists():
        lines = mqtt_jsonl.read_text(encoding="utf-8").strip().splitlines()[:5]
        (INDUSTRIAL_LOCK / "mqtt_terminal_log.txt").write_text(
            "\n".join(lines + ["Dry run only: no MQTT broker was contacted."]) + "\n",
            encoding="utf-8",
        )
    _copy_if_exists(ROOT / "production-sim-stack" / "grafana" / "industrial_service_dashboard.json", INDUSTRIAL_LOCK / "grafana_dashboard.json")
    _copy_if_exists(ROOT / "industrial-cx-ai-lab" / "ops" / "grafana_dashboard.json", INDUSTRIAL_LOCK / "grafana_dashboard_lab.json")

    docker_smoke_source = ROOT / "production-sim-stack" / "artifacts" / "docker-smoke-test.md"
    docker_smoke_json = ROOT / "production-sim-stack" / "artifacts" / "docker-smoke-test.json"
    if docker_smoke_source.exists():
        docker_md = docker_smoke_source.read_text(encoding="utf-8")
    else:
        docker_md = (
            "# Docker Smoke Test\n\n"
            "Docker Compose packaging is present in `production-sim-stack/docker-compose.yml` for API, MQTT, MLflow, MinIO, InfluxDB, and Grafana.\n\n"
            "Executed local evidence in this lock covers Python API scoring, MQTT dry-run payloads, line-protocol output, feature-mart generation, and benchmark output. Full service startup should be recorded separately when `docker compose up --build` is run.\n"
        )
    (RESULTS_DIR / "docker_smoke_test.md").write_text(docker_md, encoding="utf-8")
    (INDUSTRIAL_LOCK / "docker_smoke_test.md").write_text(docker_md, encoding="utf-8")
    _copy_if_exists(docker_smoke_json, terminal_dir / "docker_smoke_test.json")

    metrics_summary = {
        "industrial_service_risk": industrial_metrics,
        "anomaly_detection": anomaly_metrics,
        "production_simulation_rows": prod_manifest.get("rows"),
        "api_smoke_probability": api_response.get("predicted_service_escalation_probability"),
        "local_cpu_benchmark": benchmark,
        "ml_baseline": ml_metrics,
        "boundary": "Portfolio evidence only; no production industrial or employer deployment claim.",
    }
    (RESULTS_DIR / "metrics_summary.json").write_text(json.dumps(metrics_summary, indent=2, sort_keys=True), encoding="utf-8")
    (terminal_dir / "api_prediction_log.json").write_text(json.dumps(api_response, indent=2, sort_keys=True), encoding="utf-8")

    rows_per_second = benchmark.get("rows_per_second_feature_plus_scoring", "missing")
    report = f"""# Portfolio Evidence Report

Generated at: {datetime.now(timezone.utc).isoformat(timespec="seconds")}

## Executive Summary

This Evidence Lock makes the repository reviewable as an industrial Python/data-engineering portfolio project, not only as a static CX workbook. The workbook remains the communication layer; the durable evidence is telemetry generation, anomaly and service-risk scoring, MQTT dry-run output, Influx line protocol, feature-mart artifacts, API smoke evidence, Docker Compose packaging, and CPU benchmark output.

## Reproducibility

```bash
make setup
make evidence
```

Equivalent shell steps are listed in `evidence-lock/commands.sh`.

## Industrial Service Risk Evidence

| Evidence | Value |
| --- | --- |
| Service-risk F1 | {industrial_metrics.get("f1", industrial_metrics.get("metrics", {}).get("f1", "missing"))} |
| Service-risk ROC-AUC | {industrial_metrics.get("roc_auc", industrial_metrics.get("metrics", {}).get("roc_auc", "missing"))} |
| Anomaly rule F1 | {anomaly_metrics.get("rule_based", {}).get("f1", "missing")} |
| Production-sim rows | {prod_manifest.get("rows", "missing")} |
| API smoke probability | {api_response.get("predicted_service_escalation_probability", "missing")} |
| Local benchmark rows/sec | {rows_per_second} |

## BI-REX / Industrial Stack Evidence

| Artifact | Path |
| --- | --- |
| Docker smoke note | `industrial-evidence-lock/docker_smoke_test.md` |
| Grafana service screenshot | `industrial-evidence-lock/grafana_screenshot.png` |
| Grafana dashboard JSON | `industrial-evidence-lock/grafana_dashboard.json` |
| Influx line protocol sample | `industrial-evidence-lock/influx_line_protocol_sample.lp` |
| MQTT terminal log | `industrial-evidence-lock/mqtt_terminal_log.txt` |
| API prediction log | `industrial-evidence-lock/api_prediction_log.txt` |
| Feature mart output | `industrial-evidence-lock/feature_mart_duckdb_output.md` |

## Scope Boundaries

This is not a Ducati system, not a production industrial integration, not a real dealer/customer dataset, not a warranty/safety decision tool, and not a real BI-REX/CINECA/IT4LIA/PwC/CRIF deployment.
"""
    report_path = RESULTS_DIR / "portfolio_evidence_report.md"
    report_path.write_text(report, encoding="utf-8")
    return report_path


def main() -> None:
    print(build_report())


if __name__ == "__main__":
    main()
