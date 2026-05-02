from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "industrial-cx-ai-lab" / "data" / "opcua_service_events.csv"
REPORT_DIR = ROOT / "ml-baseline" / "reports"
RISK_TERMS = {
    "repeat",
    "fault",
    "complaint",
    "delayed",
    "delay",
    "warning",
    "unresolved",
    "overheating",
    "vibration",
    "pressure",
}


def require_sklearn() -> dict[str, Any]:
    try:
        from sklearn.feature_extraction import DictVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
    except ModuleNotFoundError as exc:
        raise SystemExit("Install dependencies with: python3 -m pip install -r ml-baseline/requirements.txt") from exc

    return {
        "DictVectorizer": DictVectorizer,
        "LogisticRegression": LogisticRegression,
        "accuracy_score": accuracy_score,
        "confusion_matrix": confusion_matrix,
        "f1_score": f1_score,
        "precision_score": precision_score,
        "recall_score": recall_score,
        "train_test_split": train_test_split,
        "Pipeline": Pipeline,
        "StandardScaler": StandardScaler,
    }


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def note_risk_count(note: str) -> int:
    tokens = {token.strip(".,;:!?").lower() for token in note.split()}
    return len(tokens & RISK_TERMS)


def build_features(row: dict[str, str]) -> dict[str, Any]:
    return {
        "asset_family": row["asset_family"],
        "region": row["region"],
        "vibration_rms": float(row["vibration_rms"]),
        "temperature_c": float(row["temperature_c"]),
        "battery_voltage": float(row["battery_voltage"]),
        "oil_pressure_bar": float(row["oil_pressure_bar"]),
        "service_delay_days": float(row["service_delay_days"]),
        "nps": float(row["nps"]),
        "contact_attempts": float(row["contact_attempts"]),
        "warranty_claims": float(row["warranty_claims"]),
        "telemetry_dropouts": float(row["telemetry_dropouts"]),
        "note_risk_count": note_risk_count(row["customer_note"]),
    }


def rule_baseline(row: dict[str, str]) -> int:
    return int(
        float(row["vibration_rms"]) >= 4.5
        or float(row["temperature_c"]) >= 92
        or float(row["oil_pressure_bar"]) <= 2.1
        or float(row["service_delay_days"]) >= 14
        or float(row["nps"]) <= 5
        or float(row["warranty_claims"]) >= 1
        or float(row["telemetry_dropouts"]) >= 1
        or note_risk_count(row["customer_note"]) >= 2
    )


def metric_block(metrics: dict[str, Any], expected: list[int], predicted: list[int]) -> dict[str, Any]:
    return {
        "accuracy": round(metrics["accuracy_score"](expected, predicted), 4),
        "precision": round(metrics["precision_score"](expected, predicted, zero_division=0), 4),
        "recall": round(metrics["recall_score"](expected, predicted, zero_division=0), 4),
        "f1": round(metrics["f1_score"](expected, predicted, zero_division=0), 4),
        "confusion_matrix": metrics["confusion_matrix"](expected, predicted).tolist(),
    }


def main() -> None:
    sklearn = require_sklearn()
    rows = load_rows()
    features = [build_features(row) for row in rows]
    labels = [int(row["churn_risk"]) for row in rows]

    train_test_split = sklearn["train_test_split"]
    train_x, test_x, train_y, test_y, train_rows, test_rows = train_test_split(
        features,
        labels,
        rows,
        test_size=0.3,
        random_state=42,
        stratify=labels,
    )

    model = sklearn["Pipeline"](
        [
            ("features", sklearn["DictVectorizer"](sparse=False)),
            ("scale", sklearn["StandardScaler"]()),
            ("model", sklearn["LogisticRegression"](max_iter=1000, class_weight="balanced", random_state=42)),
        ]
    )
    model.fit(train_x, train_y)

    predictions = list(model.predict(test_x))
    probabilities = [round(float(score[1]), 4) for score in model.predict_proba(test_x)]
    rule_predictions = [rule_baseline(row) for row in test_rows]

    feature_names = model.named_steps["features"].get_feature_names_out()
    coefficients = model.named_steps["model"].coef_[0]
    coefficient_rows = sorted(
        (
            {"feature": name, "coefficient": round(float(coef), 4)}
            for name, coef in zip(feature_names, coefficients)
        ),
        key=lambda item: abs(item["coefficient"]),
        reverse=True,
    )

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "task": "churn_risk",
        "data_path": str(DATA_PATH.relative_to(ROOT)),
        "model": "sklearn LogisticRegression with DictVectorizer and StandardScaler",
        "train_rows": len(train_y),
        "test_rows": len(test_y),
        "ml_metrics": metric_block(sklearn, test_y, predictions),
        "rule_baseline_metrics": metric_block(sklearn, test_y, rule_predictions),
        "top_coefficients": coefficient_rows[:8],
        "limits": [
            "Simulated data only.",
            "Small dataset for portfolio review, not production model selection.",
            "Advisory human-escalation support only.",
        ],
    }
    (REPORT_DIR / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    with (REPORT_DIR / "predictions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["event_id", "actual", "ml_prediction", "ml_probability", "rule_prediction"],
        )
        writer.writeheader()
        for row, actual, predicted, probability, rule_prediction in zip(
            test_rows,
            test_y,
            predictions,
            probabilities,
            rule_predictions,
        ):
            writer.writerow(
                {
                    "event_id": row["event_id"],
                    "actual": actual,
                    "ml_prediction": int(predicted),
                    "ml_probability": probability,
                    "rule_prediction": rule_prediction,
                }
            )

    print(
        "Scikit-learn industrial baseline completed: "
        f"rows={len(rows)} accuracy={report['ml_metrics']['accuracy']} f1={report['ml_metrics']['f1']}"
    )


if __name__ == "__main__":
    main()
