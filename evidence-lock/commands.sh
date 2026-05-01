#!/usr/bin/env bash
set -euo pipefail

python -m pip install -r requirements.txt
python -m pytest -q
python industrial-cx-ai-lab/src/run_pipeline.py
python production-sim-stack/src/orchestrate.py
python production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5
python production-sim-stack/src/api.py --example
python ml-baseline/train_model.py
python benchmarks/industrial_scoring_benchmark.py --quick
python scripts/build_evidence_report.py
