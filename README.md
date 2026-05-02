[`Live Demo`](https://errer441122.github.io/industrial-cx-service-analytics-lab/)
[![Validation](https://github.com/errer441122/industrial-cx-service-analytics-lab/actions/workflows/validate.yml/badge.svg)](https://github.com/errer441122/industrial-cx-service-analytics-lab/actions/workflows/validate.yml)

# Industrial CX & Service Analytics Lab

Simulated portfolio project combining customer-experience analytics, industrial telemetry simulation, anomaly detection, service-risk scoring and reviewer-ready AI/data evidence.

This project was originally designed as a Ducati-oriented portfolio case study. It is not affiliated with, endorsed by, or based on internal data from Ducati or any other organization. All data, telemetry, labels, dashboards and operational scenarios are simulated.

## What it demonstrates

- Customer-experience analytics workbook and dashboard storytelling.
- Data validation, KPI generation and SQL-style reporting.
- Simulated industrial telemetry generation.
- Rule-based and IsolationForest anomaly detection baseline.
- Service-risk scoring with reviewer-visible model metrics.
- MQTT/OPC UA-style contracts and Influx/Grafana-style artifacts.
- FastAPI-compatible local scoring simulation.
- Docker Compose packaging for local review.
- Slurm-ready batch scripts and local CPU benchmark.
- Explicit claims, limitations and human-review boundaries.

## Best fit

This repository is useful evidence for:

- Industrial AI / Data Engineering internships.
- Applied ML / Anomaly Detection internships.
- CX Analytics / Product Analytics roles.
- AI Product Operations roles.
- Responsible AI / Model Evidence roles.
- HPC / AI Factory readiness review.

## Reproduce

```bash
make setup
make test
make smoke
make evidence
```

Evidence report:

`evidence-lock/results/portfolio_evidence_report.md`

## Reviewer routes

| Time available | Start here |
| --- | --- |
| 5 minutes | `docs/reviewer/RECRUITER_5_MIN_ROUTE.md` |
| 20 minutes | `docs/reviewer/TECHNICAL_20_MIN_ROUTE.md` |
| Technical evidence map | `EVIDENCE_MAP.md` |
| Claims and limitations | `docs/reviewer/CLAIMS_AND_LIMITATIONS.md` |
| Original application context | `docs/application-specific/DUCATI_CX_APPLICATION_NOTE.md` |

## Role-to-evidence snapshot

| Target role area | Evidence | Honest boundary |
| --- | --- | --- |
| Industrial AI / Data Engineering | `industrial-cx-ai-lab/`, `production-sim-stack/`, `sql/`, `benchmarks/` | Simulated telemetry only; no real plant, broker, edge device or production system |
| Applied ML / Anomaly Detection | `industrial-cx-ai-lab/src/`, `ml-baseline/`, generated metrics artifacts | Synthetic labels; not validated on real industrial data |
| CX / Product Analytics | static workbook, `dashboard-workbook/`, `cx-analyst-lab/` | Simulated CX data; no real customer/dealer data |
| API / MLOps Simulation | `production-sim-stack/src/api.py`, Docker files, scoring adapter | Local simulation; not a deployed production service |
| HPC / Batch Packaging | `hpc/`, `production-sim-stack/slurm/`, `benchmarks/` | Slurm-ready packaging only; no real cluster/GPU execution |
| Responsible AI / Human Review | `docs/reviewer/CLAIMS_AND_LIMITATIONS.md`, policy notes | Advisory scoring only; no automated customer, warranty, safety or pricing decision |

## What is inside

- `index.html` - static customer-experience analytics workbook.
- `cx-data.js` - standalone simulated CX dataset and content model.
- `cx-workbook.js` - rendering logic for the CX workbook.
- `workbook-base.css` - shared workbook layout styles.
- `cx-theme.css` - project-specific CX visual layer.
- `scripts/validate-data.mjs` - local validation script for the dataset, demo wiring, navigation targets and computed KPI logic.
- `cx-analyst-lab/` - analyst technical lab with CSV validation, KPI formulas, SQL reporting views, Power BI-style model notes, customer satisfaction brief and metric tests.
- `industrial-cx-ai-lab/` - executable AI/data-engineering lab with simulated time-series telemetry, controlled anomaly injection, rule-based and IsolationForest anomaly detection, service-risk classifier, metrics, feature importance, Influx line protocol and maintenance policy note.
- `industrial-cx-ai-lab/ops/` - simulated OPC UA tag map, MQTT topic contract, Influx schema, Grafana dashboard JSON and Telegraf config sample.
- `production-sim-stack/` - local production-style simulation with FastAPI-compatible scoring, Docker Compose, MQTT dry run, MLflow-style run metadata, MinIO/S3-style artifact manifest, DuckDB mart SQL, Influx/Grafana monitoring artifacts and Slurm job array.
- `ml-baseline/` - reviewer-visible scikit-learn model baseline for industrial service-escalation scoring.
- `sql/` - top-level DuckDB mart shortcut for BI/DWH reviewers.
- `hpc/` - top-level Slurm shortcut for HPC/AI Factory-style review.
- `benchmarks/` - local CPU-only industrial scoring benchmark with generated JSON artifact.
- `docs/reviewer/` - recruiter route, technical route, limitations and role/domain reviewer notes.
- `docs/application-specific/` - optional application notes for targeted review contexts.
- `dashboard-workbook/customer_experience_dashboard.xlsx` - Excel dashboard prototype using simulated CX data.
- `PORTFOLIO_POSITIONING.md` - neutral portfolio positioning note.
- `EVIDENCE_MAP.md` - requirement-to-evidence map for recruiter and hiring-manager review.

For technical review, start with `cx-analyst-lab/`: it includes data validation, KPI generation, SQL reporting views, Power BI-style measures and metric tests.

For industrial AI review, start with `industrial-cx-ai-lab/src/run_pipeline.py`, `industrial-cx-ai-lab/artifacts/`, `industrial-cx-ai-lab/ops/` and `production-sim-stack/src/api.py`.

## Navigable demo

The `Demo guidata` section is a reviewer-facing walkthrough. It lets a reviewer select a simulated CX segment, move through journey steps, and inspect the signal, evidence, operating decision, owner, follow-up metric and output before opening the dashboard or action tracker.

## Local validation

Open `index.html` in a browser for the static demo.

Run the reproducible validation script with:

```bash
npm test
```

The validation checks dataset integrity, scoring weights, demo scenario wiring, navigation targets, computed total versus weighted insight volume and the executable Industrial CX AI lab.

Run only the workbook validation with:

```bash
npm run test:node
```

Run only the CX analyst lab with:

```bash
npm run test:cx-analyst
python3 cx-analyst-lab/src/validate_cx_data.py
python3 cx-analyst-lab/src/build_cx_summary.py
```

Run only the AI/industrial lab with:

```bash
npm run test:industrial-ai
python industrial-cx-ai-lab/src/run_pipeline.py
```

Run only the production simulation stack with:

```bash
npm run test:prod-sim
python production-sim-stack/src/orchestrate.py
python production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5
python production-sim-stack/src/api.py --example
```

Run the local CPU benchmark with:

```bash
python benchmarks/industrial_scoring_benchmark.py --quick
```

Run the scikit-learn ML baseline with:

```bash
python3 -m pip install -r ml-baseline/requirements.txt
python3 ml-baseline/train_model.py
```

The GitHub Action runs the workbook validator, Python unit tests, industrial pipeline, production simulation, MQTT dry run, scikit-learn baseline, local CPU benchmark and JSON validation for simulated industrial artifacts.

## Recommended repository metadata

- Repository name: `industrial-cx-service-analytics-lab`
- Homepage: `https://errer441122.github.io/industrial-cx-service-analytics-lab/`
- Topics: `industrial-ai`, `data-engineering`, `machine-learning`, `anomaly-detection`, `time-series`, `industrial-iot`, `fastapi`, `docker`, `scikit-learn`, `slurm`, `hpc`, `customer-analytics`, `cx`, `portfolio-project`

## Scope boundaries

This is not a Ducati system, not a production industrial integration, not a real dealer/customer dataset, not a warranty/safety/pricing decision tool and not a real cluster/HPC deployment.

All scoring outputs are advisory and designed for human review.

For the original Ducati-oriented application context, see `docs/application-specific/DUCATI_CX_APPLICATION_NOTE.md`.
