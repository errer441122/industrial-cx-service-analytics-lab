.PHONY: setup test test-node test-python industrial prod-sim benchmark json-validate smoke evidence

setup:
	python -m pip install -r requirements.txt

test: test-node test-python industrial prod-sim benchmark json-validate

test-node:
	npm test

test-python:
	python -m pytest -q

industrial:
	python industrial-cx-ai-lab/src/run_pipeline.py

prod-sim:
	python production-sim-stack/src/orchestrate.py
	python production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5
	python production-sim-stack/src/api.py --example

benchmark:
	python benchmarks/industrial_scoring_benchmark.py --quick

json-validate:
	python -m json.tool industrial-cx-ai-lab/ops/opcua_tag_map.json
	python -m json.tool industrial-cx-ai-lab/ops/grafana_dashboard.json
	python -m json.tool benchmarks/artifacts/local_cpu_benchmark.json

smoke: industrial prod-sim benchmark json-validate

evidence: test smoke
	python scripts/build_evidence_report.py
