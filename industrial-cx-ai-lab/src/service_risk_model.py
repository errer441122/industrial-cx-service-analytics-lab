from __future__ import annotations

from typing import Any

from feature_engineering import MODEL_FEATURES, labels, matrix


SERVICE_FEATURES = MODEL_FEATURES


def _binary_metrics(expected: list[int], predicted: list[int], scores: list[float]) -> dict[str, float]:
    tp = sum(1 for y, p in zip(expected, predicted) if y == 1 and p == 1)
    tn = sum(1 for y, p in zip(expected, predicted) if y == 0 and p == 0)
    fp = sum(1 for y, p in zip(expected, predicted) if y == 0 and p == 1)
    fn = sum(1 for y, p in zip(expected, predicted) if y == 1 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    metrics = {
        "accuracy": round((tp + tn) / len(expected), 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }
    try:
        from sklearn.metrics import average_precision_score, roc_auc_score

        metrics["roc_auc"] = round(float(roc_auc_score(expected, scores)), 4)
        metrics["pr_auc"] = round(float(average_precision_score(expected, scores)), 4)
    except Exception:
        metrics["roc_auc"] = 0.0
        metrics["pr_auc"] = 0.0
    return metrics


def _fallback_service_scores(rows: list[dict[str, object]]) -> list[float]:
    scores: list[float] = []
    for row in rows:
        score = min(
            1.0,
            0.28 * float(row["service_rule_score"])
            + 0.22 * min(1.0, int(row["service_delay_days"]) / 18.0)
            + 0.18 * min(1.0, int(row["error_code_count"]) / 4.0)
            + 0.16 * max(0.0, (8.0 - float(row["customer_satisfaction_score"])) / 7.0)
            + 0.16 * min(1.0, float(row["vibration_mm_s"]) / 7.0),
        )
        scores.append(round(score, 6))
    return scores


def run_service_risk_model(rows: list[dict[str, object]]) -> dict[str, Any]:
    expected = labels(rows, "service_escalation_label")
    features = matrix(rows, SERVICE_FEATURES)

    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split

        indices = list(range(len(rows)))
        train_idx, test_idx = train_test_split(
            indices,
            test_size=0.25,
            random_state=42,
            stratify=expected,
        )
        train_x = [features[index] for index in train_idx]
        train_y = [expected[index] for index in train_idx]
        test_x = [features[index] for index in test_idx]
        test_y = [expected[index] for index in test_idx]

        model = RandomForestClassifier(
            n_estimators=120,
            max_depth=6,
            min_samples_leaf=3,
            random_state=42,
            class_weight="balanced",
        )
        model.fit(train_x, train_y)
        probabilities = [float(value[1]) for value in model.predict_proba(test_x)]
        predictions = [1 if probability >= 0.5 else 0 for probability in probabilities]
        metrics = _binary_metrics(test_y, predictions, probabilities)
        feature_importance = [
            {"feature": name, "importance": round(float(value), 6)}
            for name, value in zip(SERVICE_FEATURES, model.feature_importances_)
        ]
        model_name = "sklearn.ensemble.RandomForestClassifier"
        test_rows = len(test_y)
    except Exception as exc:
        probabilities = _fallback_service_scores(rows)
        predictions = [1 if probability >= 0.5 else 0 for probability in probabilities]
        metrics = _binary_metrics(expected, predictions, probabilities)
        feature_importance = [
            {"feature": "service_rule_score", "importance": 0.28},
            {"feature": "service_delay_days", "importance": 0.22},
            {"feature": "error_code_count", "importance": 0.18},
            {"feature": "customer_satisfaction_score", "importance": 0.16},
            {"feature": "vibration_mm_s", "importance": 0.16},
        ]
        model_name = f"fallback_weighted_baseline: {exc}"
        test_rows = len(expected)

    feature_importance.sort(key=lambda item: item["importance"], reverse=True)

    return {
        "model": model_name,
        "rows": len(rows),
        "test_rows": test_rows,
        "positive_service_escalation_labels": sum(expected),
        "target": "service_escalation_label",
        "metrics": metrics,
        **metrics,
        "feature_importance": feature_importance,
        "disclaimer": (
            "Synthetic local service-risk classifier only; not a production "
            "industrial, warranty, safety, pricing, or customer-treatment model."
        ),
    }
