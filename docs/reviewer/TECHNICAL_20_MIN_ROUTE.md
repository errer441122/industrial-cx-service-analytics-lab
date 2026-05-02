# Technical 20-Minute Route

This route verifies the executable evidence behind the repository claims. All commands are local CPU checks using simulated data.

## 1. Run The Core Checks

```bash
npm test
python -m pytest -q
python industrial-cx-ai-lab/src/run_pipeline.py
python production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5
python benchmarks/industrial_scoring_benchmark.py --quick
```

## 2. Inspect Industrial AI Outputs

| Artifact | What it proves |
| --- | --- |
| `industrial-cx-ai-lab/data/simulated_telemetry.csv` | deterministic time-series telemetry with expected fields |
| `industrial-cx-ai-lab/artifacts/anomaly_metrics.json` | rule baseline plus IsolationForest anomaly metrics |
| `industrial-cx-ai-lab/artifacts/service_risk_metrics.json` | service-risk classifier metrics |
| `industrial-cx-ai-lab/artifacts/feature_importance.csv` | feature importance for reviewer inspection |
| `industrial-cx-ai-lab/artifacts/influx_line_protocol.txt` | local Influx line protocol export |
| `industrial-cx-ai-lab/artifacts/maintenance_policy_note.md` | human-in-the-loop policy boundary |

## 3. Inspect Simulated Industrial Data Contracts

| File | Boundary |
| --- | --- |
| `industrial-cx-ai-lab/ops/opcua_tag_map.json` | simulated OPC UA-style nodes only |
| `industrial-cx-ai-lab/ops/mqtt_topics.json` | simulated MQTT topic contract only |
| `industrial-cx-ai-lab/ops/influx_schema.md` | schema design only |
| `industrial-cx-ai-lab/ops/grafana_dashboard.json` | dashboard JSON design artifact |
| `industrial-cx-ai-lab/ops/telegraf_config_sample.conf` | sample config, not executed against a real broker |

## 4. Inspect API And Production Simulation

Minimum scoring surface:

- `production-sim-stack/src/model_adapter.py`
- `production-sim-stack/src/api.py`
- `production-sim-stack/docs/architecture.md`
- `production-sim-stack/docs/smoke_test_plan.md`

Optional local API example:

```bash
python production-sim-stack/src/api.py --example
```

## 5. Inspect HPC / Benchmark Evidence

| File | Meaning |
| --- | --- |
| `hpc/run_industrial_scoring_array.sbatch` | Slurm-ready packaging only |
| `benchmarks/industrial_scoring_benchmark.py` | local CPU timing path |
| `benchmarks/artifacts/local_cpu_benchmark.json` | generated local benchmark artifact |

No real cluster, cloud, GPU, edge, partner, production or Slurm execution is claimed.
