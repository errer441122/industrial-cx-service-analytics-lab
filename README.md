[`Live Demo`](https://errer441122.github.io/ducati-cx-case-study/)  
[![Live Site](https://img.shields.io/badge/Live%20Site-GitHub%20Pages-CC0000?style=for-the-badge)](https://errer441122.github.io/ducati-cx-case-study/)
[![Validation](https://github.com/errer441122/ducati-cx-case-study/actions/workflows/validate.yml/badge.svg)](https://github.com/errer441122/ducati-cx-case-study/actions/workflows/validate.yml)

# Ducati CX Analytics Workbook

This repository is a standalone Customer Experience analytics workbook. The center of gravity is simulated customer data, Excel dashboarding, journey friction analysis, segmentation, and action tracking for a Data Analyst Customer Experience application.

## What is inside

- `index.html` - open this to review the Customer Experience analytics workbook.
- `cx-data.js` - standalone Ducati/CX simulated dataset and content model.
- `cx-workbook.js` - rendering logic for the CX workbook.
- `workbook-base.css` - shared workbook layout styles.
- `cx-theme.css` - Ducati/CX-specific visual layer.
- `scripts/validate-data.mjs` - local validation script for the dataset, demo wiring, navigation targets, and computed KPI logic.
- `cx-analyst-lab/` - analyst technical lab with CSV validation, KPI formulas, SQL reporting views, Power BI-style model notes, customer satisfaction brief, and metric tests.
- `industrial-cx-ai-lab/` - executable AI/data-engineering lab with simulated OPC UA-style telemetry, anomaly features, churn/service-risk classifier, SQLite feature mart, Influx export, Grafana panel stub, and Slurm batch script.
- `production-sim-stack/` - `8/10` upgrade layer with FastAPI scoring, Docker Compose, MQTT simulation, MLflow-style run metadata, MinIO/S3-style artifact manifest, DuckDB mart SQL, Influx/Grafana monitoring artifacts, and Slurm job array.
- `ml-baseline/` - reviewer-visible scikit-learn model baseline for industrial service-escalation scoring.
- `sql/` - top-level DuckDB mart shortcut for BI/DWH reviewers.
- `hpc/` - top-level Slurm shortcut for CINECA/IT4LIA/BI-REX-style review.
- `dashboard-workbook/customer_experience_dashboard.xlsx` - Excel dashboard prototype using simulated CX data.
- `PROJECT_POSITIONING.md` - short explanation of how to present the project for the Ducati role.
- `EVIDENCE_MAP.md` - requirement-to-evidence map for recruiter and hiring-manager review.
- `AI_INTERNSHIP_FIT.md` - strict note explaining why this is secondary evidence for AI/data internships, not the main AI engineering project.

For technical review, start with `cx-analyst-lab/`: it includes data validation, KPI generation, SQL reporting views, Power BI-style measures, and metric tests.

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
python3 industrial-cx-ai-lab/src/run_pipeline.py
```

Run only the production simulation stack with:

```bash
npm run test:prod-sim
python3 production-sim-stack/src/orchestrate.py
python3 production-sim-stack/src/mqtt_simulator.py
```

Run the scikit-learn ML baseline with:

```bash
python3 -m pip install -r ml-baseline/requirements.txt
python3 ml-baseline/train_model.py
```

The GitHub Action runs the workbook validator, Python unit tests, industrial pipeline, production simulation, MQTT simulator, and scikit-learn baseline.

## Recommended repository metadata

- Homepage: `https://errer441122.github.io/ducati-cx-case-study/`
- Topics: `customer-analytics`, `data-analysis`, `dashboard`, `excel`, `cx`, `portfolio-project`, `customer-experience`, `segmentation`, `industrial-iot`, `machine-learning`, `opc-ua`

## Positioning for the application

Use this version as a Customer Experience Data Analyst portfolio piece. The strongest angle is:

> I built a Customer Experience analytics workbook showing how I would collect, organize and analyze customer feedback, build dashboard views, segment customers, identify journey trends and translate findings into clear improvement actions.

The project uses simulated data only. It does not claim access to Ducati systems, Ducati customer data, dealer data or internal processes.

The project is not intended to simulate Ducati internal data. It is a portfolio case study showing how I would structure a CX analytics workflow if approved survey, CRM, service, dealer or digital-touchpoint data were available.

For AI/data internships, use `industrial-cx-ai-lab/` and `production-sim-stack/` as the technical supplement. The original workbook remains the communication layer; the labs are the evidence for ML, Industrial IoT-style data, MQTT/OPC UA-style messaging, time-series monitoring, MLOps-style lifecycle, and HPC-style batch packaging.
