# Scikit-learn Industrial Service Baseline

This folder makes the machine-learning evidence explicit for BI-REX, PwC Data & AI, and CRIF-style technical review.

The task is advisory: predict whether a simulated after-sales / industrial telemetry event should be escalated to human service review. It does not automate warranty, customer, dealer, or commercial decisions.

## What It Shows

- Python ML workflow using scikit-learn.
- Train/test split with deterministic random seed.
- Logistic regression baseline.
- Rule-based baseline for comparison.
- Accuracy, precision, recall, F1, confusion matrix, and coefficient export.
- Reproducible report output under `ml-baseline/reports/`.

## Run

```bash
python3 -m pip install -r ml-baseline/requirements.txt
python3 ml-baseline/train_model.py
```

The GitHub Action installs the dependency and runs this baseline as part of validation.

## Boundary

This is a portfolio-scale baseline. The production-like industrial simulation is in `production-sim-stack/`.
