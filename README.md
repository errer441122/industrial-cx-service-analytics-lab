# Industrial CX & Service Analytics Workbook

[`Static Demo`](https://errer441122.github.io/ducati-cx-case-study/)
[![Live Site](https://img.shields.io/badge/Live%20Site-GitHub%20Pages-CC0000?style=for-the-badge)](https://errer441122.github.io/ducati-cx-case-study/)
[![Validation](https://github.com/errer441122/ducati-cx-case-study/actions/workflows/validate.yml/badge.svg)](https://github.com/errer441122/ducati-cx-case-study/actions/workflows/validate.yml)

## Evidence Lock v1.0

This repository is a customer-experience workbook plus an executable industrial analytics evidence package.

### What is executable

- Python industrial telemetry generator
- Service-risk and anomaly scoring baseline
- MQTT dry-run payload generator
- Influx line protocol output
- DuckDB/SQLite-style feature mart artifacts
- FastAPI-compatible scoring simulation
- Docker Compose packaging for API, MQTT, MLflow, MinIO, InfluxDB, and Grafana
- Slurm-ready industrial scoring batch scripts
- Local CPU benchmark for industrial AI / HPC-style review

### Reproduce

```bash
make setup
make evidence
```

Evidence report: `evidence-lock/results/portfolio_evidence_report.md`

Scope boundaries: this is not a production industrial integration, not a real dealer/customer dataset, not a warranty/safety decision tool, and not a real client, partner, cloud, HPC, or employer deployment.

## Technical evidence

Primary stack: Python, scikit-learn, industrial time-series simulation, MQTT/OPC UA-style contracts, Influx/Grafana artifacts, FastAPI-compatible API, Docker, Slurm-ready batch scripts.

Run:

```bash
make setup
make test
make smoke
make evidence
```

## Portfolio positioning

A simulated portfolio case study combining customer experience analytics with an industrial-service AI lab: telemetry simulation, anomaly detection, service-risk scoring, MQTT/OPC UA-style artifacts, Influx/Grafana monitoring stubs, FastAPI-compatible local scoring, DuckDB SQL, and Slurm-ready batch packaging.

Best for: industrial AI support, consulting data and responsible AI storytelling, product/CX analytics, and HPC-style workload packaging review.

What is executable: `npm test`, `python -m pytest -q`, `python industrial-cx-ai-lab/src/run_pipeline.py`, `python production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5`, and `python benchmarks/industrial_scoring_benchmark.py --quick`.

What is simulated: all branded CX data, telemetry, anomaly labels, service-risk labels, OPC UA/MQTT/Influx/Grafana designs, FastAPI scoring, Docker services, Slurm/HPC packaging, and cloud/edge context.

Start here if you have 5 minutes: `docs/reviewer/RECRUITER_5_MIN_ROUTE.md`.

This is not a production industrial integration, not a real dealer/customer dataset, not a warranty/safety decision tool, and not the main regulated AI or public-sector engineering project.

## Role-to-evidence snapshot

| Role | Evidence | What not to claim |
| --- | --- | --- |
| Industrial AI / Data Engineering | `industrial-cx-ai-lab/`, `industrial-cx-ai-lab/ops/`, `production-sim-stack/`, `hpc/`, `benchmarks/` | No real plant, edge, OPC UA, MQTT, Influx, Grafana, Slurm, or partner execution |
| Consulting Data & Responsible AI | CX workbook, `cx-analyst-lab/`, `sql/`, `docs/reviewer/CONSULTING_DATA_AI_STORY.md` | No client engagement or production dashboard deployment |
| HPC / AI Factory supplement | Slurm scripts, local CPU benchmark, Docker/local stack docs | No real cluster, GPU, Leonardo, or AI Factory access |
| Financial-risk support evidence | transparent scoring limits, `ml-baseline/`, data-quality validation | Secondary evidence only, no financial-services data or regulated credit model |

## What is inside

- `index.html` - open this to review the Customer Experience analytics workbook.
- `cx-data.js` - standalone simulated CX dataset and content model.
- `cx-workbook.js` - rendering logic for the CX workbook.
- `workbook-base.css` - shared workbook layout styles.
- `cx-theme.css` - project-specific CX visual layer.
- `scripts/validate-data.mjs` - local validation script for the dataset, demo wiring, navigation targets, and computed KPI logic.
- `cx-analyst-lab/` - analyst technical lab with CSV validation, KPI formulas, SQL reporting views, Power BI-style model notes, customer satisfaction brief, and metric tests.
- `industrial-cx-ai-lab/` - executable AI/data-engineering lab with simulated time-series telemetry, controlled anomaly injection, rule-based and IsolationForest anomaly detection, service-risk classifier, metrics, feature importance, Influx line protocol, and maintenance policy note.
- `industrial-cx-ai-lab/ops/` - simulated OPC UA tag map, MQTT topic contract, Influx schema, Grafana dashboard JSON, and Telegraf config sample.
- `production-sim-stack/` - local production-style simulation with FastAPI-compatible scoring, Docker Compose, MQTT dry run, MLflow-style run metadata, MinIO/S3-style artifact manifest, DuckDB mart SQL, Influx/Grafana monitoring artifacts, and Slurm job array.
- `ml-baseline/` - reviewer-visible scikit-learn model baseline for industrial service-escalation scoring.
- `sql/` - top-level DuckDB mart shortcut for BI/DWH reviewers.
- `hpc/` - top-level Slurm shortcut for HPC/AI Factory-style review.
- `benchmarks/` - local CPU-only industrial scoring benchmark with generated JSON artifact.
- `docs/reviewer/` - recruiter route, technical route, limitations, company fit matrix, and industrial/consulting story docs.
- `dashboard-workbook/customer_experience_dashboard.xlsx` - Excel dashboard prototype using simulated CX data.
- `PROJECT_POSITIONING.md` - application-specific positioning note for the original branded context.
- `EVIDENCE_MAP.md` - requirement-to-evidence map for recruiter and hiring-manager review.
- `AI_INTERNSHIP_FIT.md` - strict note explaining why this is secondary evidence for AI/data internships, not the main AI engineering project.

For technical review, start with `cx-analyst-lab/`: it includes data validation, KPI generation, SQL reporting views, Power BI-style measures, and metric tests.

For industrial AI review, start with `industrial-cx-ai-lab/src/run_pipeline.py`, `industrial-cx-ai-lab/artifacts/`, `industrial-cx-ai-lab/ops/`, and `production-sim-stack/src/api.py`.

## Navigable demo

The `Demo guidata` section is a reviewer-facing walkthrough. It lets a reviewer select a simulated CX segment, move through journey steps, and inspect the signal, evidence, operating decision, owner, follow-up metric, and output before opening the dashboard or action tracker.

## Local validation

Open `index.html` in a browser for the static demo.

Run the reproducible validation script with:

```bash
npm test
```

The validation checks dataset integrity, scoring weights, demo scenario wiring, navigation targets, computed total versus weighted insight volume, and the executable Industrial CX AI lab.

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

The GitHub Action runs the workbook validator, Python unit tests, industrial pipeline, production simulation, MQTT dry run, scikit-learn baseline, local CPU benchmark, and JSON validation for simulated industrial artifacts.

## Recommended repository metadata

- Homepage: `https://errer441122.github.io/ducati-cx-case-study/`
- Recommended neutral repository name: `industrial-cx-service-analytics-workbook`
- Topics: `customer-analytics`, `data-analysis`, `dashboard`, `excel`, `cx`, `portfolio-project`, `customer-experience`, `segmentation`, `industrial-iot`, `machine-learning`, `opc-ua`

## Original Application Context

Originally designed as a Ducati-oriented portfolio case study using simulated data only.

For the original Customer Experience Data Analyst application, use this as a CX analytics portfolio piece. The strongest angle is:

> I built a Customer Experience analytics workbook showing how I would collect, organize and analyze customer feedback, build dashboard views, segment customers, identify journey trends and translate findings into clear improvement actions.

The project uses simulated data only. It does not claim access to Ducati systems, Ducati customer data, dealer data or internal processes.

The project is not intended to simulate Ducati internal data. It is a portfolio case study showing how I would structure a CX analytics workflow if approved survey, CRM, service, dealer or digital-touchpoint data were available.

For industrial AI, consulting data, or HPC-style AI/data internships, use `industrial-cx-ai-lab/`, `production-sim-stack/`, `hpc/`, and `benchmarks/` as the technical supplement. The original workbook remains the communication layer; the labs are the evidence for ML, Industrial IoT-style data, MQTT/OPC UA-style messaging, time-series monitoring, MLOps-style lifecycle, and HPC-style batch packaging.
