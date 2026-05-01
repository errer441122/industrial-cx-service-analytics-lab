from __future__ import annotations

import csv
import json
import math
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "opcua_service_events.csv"
ARTIFACT_DIR = BASE_DIR / "artifacts"

REQUIRED_COLUMNS = {
    "event_id",
    "bike_family",
    "region",
    "timestamp",
    "opcua_node",
    "vibration_rms",
    "temperature_c",
    "battery_voltage",
    "oil_pressure_bar",
    "service_delay_days",
    "nps",
    "contact_attempts",
    "warranty_claims",
    "telemetry_dropouts",
    "customer_note",
    "churn_risk",
}

RISK_TERMS = {
    "alarm",
    "breakdown",
    "complaint",
    "critical",
    "delay",
    "delayed",
    "escalation",
    "fault",
    "overheating",
    "repeat",
    "unresolved",
    "vibration",
    "warning",
}

FEATURE_NAMES = [
    "vibration_rms",
    "temperature_c",
    "battery_voltage",
    "oil_pressure_bar",
    "service_delay_days",
    "nps",
    "contact_attempts",
    "warranty_claims",
    "telemetry_dropouts",
    "text_risk_hits",
    "telemetry_anomaly_score",
]


@dataclass
class ModelBundle:
    feature_names: list[str]
    weights: list[float]
    means: list[float]
    scales: list[float]
    threshold: float = 0.5


def _to_float(value: str, column: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Column {column} must be numeric, got {value!r}") from exc


def _to_int(value: str, column: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Column {column} must be an integer, got {value!r}") from exc


def load_rows(path: Path = DATA_PATH) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        rows: list[dict[str, object]] = []
        for raw in reader:
            rows.append(
                {
                    "event_id": raw["event_id"],
                    "bike_family": raw["bike_family"],
                    "region": raw["region"],
                    "timestamp": raw["timestamp"],
                    "opcua_node": raw["opcua_node"],
                    "vibration_rms": _to_float(raw["vibration_rms"], "vibration_rms"),
                    "temperature_c": _to_float(raw["temperature_c"], "temperature_c"),
                    "battery_voltage": _to_float(raw["battery_voltage"], "battery_voltage"),
                    "oil_pressure_bar": _to_float(raw["oil_pressure_bar"], "oil_pressure_bar"),
                    "service_delay_days": _to_int(raw["service_delay_days"], "service_delay_days"),
                    "nps": _to_int(raw["nps"], "nps"),
                    "contact_attempts": _to_int(raw["contact_attempts"], "contact_attempts"),
                    "warranty_claims": _to_int(raw["warranty_claims"], "warranty_claims"),
                    "telemetry_dropouts": _to_int(raw["telemetry_dropouts"], "telemetry_dropouts"),
                    "customer_note": raw["customer_note"],
                    "churn_risk": _to_int(raw["churn_risk"], "churn_risk"),
                }
            )

    if len(rows) < 24:
        raise ValueError("The lab needs at least 24 rows for a meaningful train/test split.")
    return rows


def count_text_risk_hits(text: str) -> int:
    tokens = {token.strip(".,:;()[]").lower() for token in text.split()}
    return len(tokens & RISK_TERMS)


def enrich_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    telemetry_columns = ["vibration_rms", "temperature_c", "battery_voltage", "oil_pressure_bar"]
    means = {column: mean(float(row[column]) for row in rows) for column in telemetry_columns}
    scales = {column: pstdev(float(row[column]) for row in rows) or 1.0 for column in telemetry_columns}

    enriched: list[dict[str, object]] = []
    for row in rows:
        z_scores = [
            abs((float(row[column]) - means[column]) / scales[column])
            for column in telemetry_columns
        ]
        next_row = dict(row)
        next_row["text_risk_hits"] = count_text_risk_hits(str(row["customer_note"]))
        next_row["telemetry_anomaly_score"] = round(sum(z_scores) / len(z_scores), 4)
        enriched.append(next_row)
    return enriched


def build_matrix(rows: list[dict[str, object]]) -> tuple[list[list[float]], list[int]]:
    features = [[float(row[name]) for name in FEATURE_NAMES] for row in rows]
    labels = [int(row["churn_risk"]) for row in rows]
    return features, labels


def split_train_test(features: list[list[float]], labels: list[int]) -> tuple[list[list[float]], list[int], list[list[float]], list[int]]:
    train_x: list[list[float]] = []
    train_y: list[int] = []
    test_x: list[list[float]] = []
    test_y: list[int] = []

    for index, (feature_row, label) in enumerate(zip(features, labels)):
        if index % 5 == 0:
            test_x.append(feature_row)
            test_y.append(label)
        else:
            train_x.append(feature_row)
            train_y.append(label)
    return train_x, train_y, test_x, test_y


def fit_standardizer(features: list[list[float]]) -> tuple[list[float], list[float]]:
    columns = list(zip(*features))
    means = [mean(column) for column in columns]
    scales = [pstdev(column) or 1.0 for column in columns]
    return means, scales


def transform(features: list[list[float]], means: list[float], scales: list[float]) -> list[list[float]]:
    return [
        [(value - means[index]) / scales[index] for index, value in enumerate(row)]
        for row in features
    ]


def sigmoid(value: float) -> float:
    if value < -35:
        return 0.0
    if value > 35:
        return 1.0
    return 1.0 / (1.0 + math.exp(-value))


def train_logistic_regression(
    features: list[list[float]],
    labels: list[int],
    epochs: int = 1800,
    learning_rate: float = 0.08,
    l2_penalty: float = 0.001,
) -> list[float]:
    weights = [0.0 for _ in range(len(features[0]) + 1)]
    sample_count = len(labels)

    for _ in range(epochs):
        gradients = [0.0 for _ in weights]
        for row, label in zip(features, labels):
            score = weights[0] + sum(weight * value for weight, value in zip(weights[1:], row))
            error = sigmoid(score) - label
            gradients[0] += error
            for index, value in enumerate(row, start=1):
                gradients[index] += error * value

        for index in range(len(weights)):
            regularization = 0.0 if index == 0 else l2_penalty * weights[index]
            weights[index] -= learning_rate * ((gradients[index] / sample_count) + regularization)
    return weights


def predict_probabilities(features: list[list[float]], weights: list[float]) -> list[float]:
    return [
        sigmoid(weights[0] + sum(weight * value for weight, value in zip(weights[1:], row)))
        for row in features
    ]


def evaluate(labels: list[int], probabilities: list[float], threshold: float = 0.5) -> dict[str, float]:
    predictions = [1 if probability >= threshold else 0 for probability in probabilities]
    tp = sum(1 for expected, actual in zip(labels, predictions) if expected == 1 and actual == 1)
    tn = sum(1 for expected, actual in zip(labels, predictions) if expected == 0 and actual == 0)
    fp = sum(1 for expected, actual in zip(labels, predictions) if expected == 0 and actual == 1)
    fn = sum(1 for expected, actual in zip(labels, predictions) if expected == 1 and actual == 0)

    accuracy = (tp + tn) / len(labels)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }


def write_sqlite_mart(rows: list[dict[str, object]], probabilities: list[float], output_dir: Path) -> Path:
    mart_path = output_dir / "industrial_cx_feature_mart.sqlite"
    if mart_path.exists():
        mart_path.unlink()

    with closing(sqlite3.connect(mart_path)) as connection:
        connection.execute(
            """
            CREATE TABLE industrial_cx_features (
                event_id TEXT PRIMARY KEY,
                bike_family TEXT NOT NULL,
                region TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                opcua_node TEXT NOT NULL,
                vibration_rms REAL NOT NULL,
                temperature_c REAL NOT NULL,
                battery_voltage REAL NOT NULL,
                oil_pressure_bar REAL NOT NULL,
                service_delay_days INTEGER NOT NULL,
                nps INTEGER NOT NULL,
                contact_attempts INTEGER NOT NULL,
                warranty_claims INTEGER NOT NULL,
                telemetry_dropouts INTEGER NOT NULL,
                text_risk_hits INTEGER NOT NULL,
                telemetry_anomaly_score REAL NOT NULL,
                predicted_churn_probability REAL NOT NULL,
                churn_risk INTEGER NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO industrial_cx_features VALUES (
                :event_id,
                :bike_family,
                :region,
                :timestamp,
                :opcua_node,
                :vibration_rms,
                :temperature_c,
                :battery_voltage,
                :oil_pressure_bar,
                :service_delay_days,
                :nps,
                :contact_attempts,
                :warranty_claims,
                :telemetry_dropouts,
                :text_risk_hits,
                :telemetry_anomaly_score,
                :predicted_churn_probability,
                :churn_risk
            )
            """,
            [
                {
                    **row,
                    "predicted_churn_probability": round(probability, 4),
                }
                for row, probability in zip(rows, probabilities)
            ],
        )
        connection.commit()
    return mart_path


def write_influx_export(rows: list[dict[str, object]], probabilities: list[float], output_dir: Path) -> Path:
    output_path = output_dir / "service_risk_influx.lp"
    lines = []
    for row, probability in zip(rows, probabilities):
        tags = f"bike_family={row['bike_family']},region={row['region']}"
        fields = (
            f"predicted_churn_probability={round(probability, 4)},"
            f"telemetry_anomaly_score={row['telemetry_anomaly_score']},"
            f"service_delay_days={row['service_delay_days']}i"
        )
        timestamp_ns = int(datetime.fromisoformat(str(row["timestamp"]).replace("Z", "+00:00")).timestamp() * 1_000_000_000)
        lines.append(f"ducati_service_risk,{tags} {fields} {timestamp_ns}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def write_artifacts(
    rows: list[dict[str, object]],
    probabilities: list[float],
    metrics: dict[str, float],
    bundle: ModelBundle,
    output_dir: Path,
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    predictions_path = output_dir / "industrial_cx_predictions.csv"
    with predictions_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "event_id",
            "bike_family",
            "region",
            "predicted_churn_probability",
            "predicted_human_review",
            "churn_risk",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row, probability in zip(rows, probabilities):
            writer.writerow(
                {
                    "event_id": row["event_id"],
                    "bike_family": row["bike_family"],
                    "region": row["region"],
                    "predicted_churn_probability": round(probability, 4),
                    "predicted_human_review": int(probability >= bundle.threshold),
                    "churn_risk": row["churn_risk"],
                }
            )

    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")

    model_card_path = output_dir / "model_card.json"
    model_card = {
        "model_name": "industrial_cx_service_risk_classifier",
        "model_type": "logistic_regression_from_scratch",
        "target": "churn_risk",
        "decision_boundary": "advisory service triage only",
        "feature_names": bundle.feature_names,
        "metrics": metrics,
        "limitations": [
            "simulated data only",
            "no real Ducati telemetry",
            "small sample size",
            "not calibrated for commercial action",
            "no live OPC UA, InfluxDB, Grafana, Slurm, or cloud execution",
        ],
    }
    model_card_path.write_text(json.dumps(model_card, indent=2, sort_keys=True), encoding="utf-8")

    manifest_path = output_dir / "run_manifest.json"
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": len(rows),
        "artifacts": [
            str(predictions_path.name),
            str(metrics_path.name),
            str(model_card_path.name),
            "industrial_cx_feature_mart.sqlite",
            "service_risk_influx.lp",
        ],
        "review_boundary": "human service owner must review any escalation recommendation",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    influx_path = write_influx_export(rows, probabilities, output_dir)

    return {
        "predictions": str(predictions_path),
        "metrics": str(metrics_path),
        "model_card": str(model_card_path),
        "manifest": str(manifest_path),
        "influx": str(influx_path),
    }


def run_pipeline(output_dir: Path = ARTIFACT_DIR) -> dict[str, object]:
    rows = enrich_rows(load_rows())
    features, labels = build_matrix(rows)
    train_x, train_y, test_x, test_y = split_train_test(features, labels)

    means, scales = fit_standardizer(train_x)
    train_x_scaled = transform(train_x, means, scales)
    test_x_scaled = transform(test_x, means, scales)
    all_x_scaled = transform(features, means, scales)

    weights = train_logistic_regression(train_x_scaled, train_y)
    test_probabilities = predict_probabilities(test_x_scaled, weights)
    all_probabilities = predict_probabilities(all_x_scaled, weights)
    metrics = evaluate(test_y, test_probabilities)

    bundle = ModelBundle(
        feature_names=FEATURE_NAMES,
        weights=[round(weight, 6) for weight in weights],
        means=[round(value, 6) for value in means],
        scales=[round(value, 6) for value in scales],
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    mart_path = write_sqlite_mart(rows, all_probabilities, output_dir)
    artifacts = write_artifacts(rows, all_probabilities, metrics, bundle, output_dir)

    return {
        "rows": len(rows),
        "metrics": metrics,
        "model": bundle,
        "mart": str(mart_path),
        "artifacts": artifacts,
    }


def main() -> None:
    result = run_pipeline()
    metrics = result["metrics"]
    print(
        "Industrial CX AI lab completed: "
        f"rows={result['rows']} "
        f"accuracy={metrics['accuracy']} "
        f"f1={metrics['f1']}"
    )


if __name__ == "__main__":
    main()
