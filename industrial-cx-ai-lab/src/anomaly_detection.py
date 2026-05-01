from __future__ import annotations

from typing import Any

from feature_engineering import MODEL_FEATURES, labels, matrix


ANOMALY_FEATURES = [
    "rpm",
    "temperature_c",
    "vibration_mm_s",
    "pressure_bar",
    "torque_nm",
    "operating_hours",
    "error_code_count",
    "service_delay_days",
    "temperature_over_85",
    "vibration_over_5",
    "pressure_under_2",
    "error_burst_flag",
    "maintenance_delay_flag",
]


def rule_based_anomaly_predictions(rows: list[dict[str, object]]) -> list[int]:
    predictions: list[int] = []
    for row in rows:
        predictions.append(
            int(
                float(row["temperature_c"]) >= 88.0
                or float(row["vibration_mm_s"]) >= 5.2
                or float(row["pressure_bar"]) <= 1.75
                or int(row["error_code_count"]) >= 3
                or int(row["service_delay_days"]) >= 14
            )
        )
    return predictions


def _basic_binary_metrics(expected: list[int], predicted: list[int]) -> dict[str, float]:
    tp = sum(1 for y, p in zip(expected, predicted) if y == 1 and p == 1)
    tn = sum(1 for y, p in zip(expected, predicted) if y == 0 and p == 0)
    fp = sum(1 for y, p in zip(expected, predicted) if y == 0 and p == 1)
    fn = sum(1 for y, p in zip(expected, predicted) if y == 1 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": round((tp + tn) / len(expected), 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }


def _metrics(expected: list[int], predicted: list[int], scores: list[float] | None = None) -> dict[str, float]:
    result = _basic_binary_metrics(expected, predicted)
    if scores is None:
        return result

    try:
        from sklearn.metrics import average_precision_score, roc_auc_score

        result["roc_auc"] = round(float(roc_auc_score(expected, scores)), 4)
        result["pr_auc"] = round(float(average_precision_score(expected, scores)), 4)
    except Exception:
        result["roc_auc"] = 0.0
        result["pr_auc"] = 0.0
    return result


def _normalize_scores(values: list[float]) -> list[float]:
    lower = min(values)
    upper = max(values)
    if upper == lower:
        return [0.0 for _ in values]
    return [round((value - lower) / (upper - lower), 6) for value in values]


def run_anomaly_detection(rows: list[dict[str, object]]) -> dict[str, Any]:
    expected = labels(rows, "anomaly_label")
    rule_predictions = rule_based_anomaly_predictions(rows)
    rule_scores = [float(row["service_rule_score"]) for row in rows]

    report: dict[str, Any] = {
        "dataset": {
            "rows": len(rows),
            "positive_anomaly_labels": sum(expected),
            "simulation_boundary": "Synthetic labels from controlled anomaly injection.",
        },
        "rule_based": _metrics(expected, rule_predictions, rule_scores),
    }

    try:
        from sklearn.ensemble import IsolationForest

        feature_matrix = matrix(rows, ANOMALY_FEATURES)
        contamination = min(max(sum(expected) / len(expected), 0.05), 0.25)
        model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42,
        )
        model_predictions = [1 if value == -1 else 0 for value in model.fit_predict(feature_matrix)]
        raw_scores = [-float(value) for value in model.decision_function(feature_matrix)]
        normalized_scores = _normalize_scores(raw_scores)
        report["isolation_forest"] = {
            "model": "sklearn.ensemble.IsolationForest",
            "contamination": round(contamination, 4),
            **_metrics(expected, model_predictions, normalized_scores),
        }
    except Exception as exc:
        report["isolation_forest"] = {
            "model": "fallback_rule_based_copy",
            "dependency_note": f"IsolationForest unavailable: {exc}",
            **_metrics(expected, rule_predictions, rule_scores),
        }

    report["feature_set"] = ANOMALY_FEATURES
    report["disclaimer"] = (
        "Local CPU simulation only; no real OPC UA, MQTT, Influx, Grafana, "
        "Ducati, plant, dealer, or production telemetry integration."
    )
    return report
