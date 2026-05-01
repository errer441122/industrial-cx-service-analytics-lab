from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from validate_cx_data import DATA_PATH, load_rows, validate_rows


def _int(row: dict[str, str], field: str) -> int:
    return int(row[field])


def _weighted_average(rows: list[dict[str, str]], value_field: str) -> float:
    total_volume = sum(_int(row, "feedback_volume") for row in rows)
    if total_volume == 0:
        return 0.0
    weighted_sum = sum(_int(row, value_field) * _int(row, "feedback_volume") for row in rows)
    return round(weighted_sum / total_volume, 2)


def group_by(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row[field]].append(row)
    return dict(grouped)


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    errors = validate_rows(rows)
    if errors:
        raise ValueError("; ".join(errors))

    total_volume = sum(_int(row, "feedback_volume") for row in rows)
    satisfied_volume = sum(
        _int(row, "feedback_volume") for row in rows if _int(row, "satisfaction_score") >= 4
    )
    follow_up_required = [row for row in rows if row["follow_up_required"].lower() == "yes"]
    follow_up_completed = [row for row in follow_up_required if row["follow_up_completed"].lower() == "yes"]
    completed_delta_rows = [
        {
            **row,
            "delta": _int(row, "post_action_score") - _int(row, "satisfaction_score"),
        }
        for row in follow_up_completed
    ]

    segment_summary = {}
    for segment, segment_rows in group_by(rows, "segment").items():
        segment_summary[segment] = {
            "feedback_volume": sum(_int(row, "feedback_volume") for row in segment_rows),
            "avg_satisfaction": _weighted_average(segment_rows, "satisfaction_score"),
            "avg_friction": _weighted_average(segment_rows, "friction_score"),
        }

    at_risk_segments = [
        segment
        for segment, metrics in segment_summary.items()
        if metrics["avg_satisfaction"] < 3.5 or metrics["avg_friction"] >= 3.5
    ]

    month_summary = {}
    for month, month_rows in group_by(rows, "date").items():
        month_key = month[:7]
        month_summary.setdefault(month_key, {"feedback_volume": 0, "rows": []})
        month_summary[month_key]["feedback_volume"] += sum(_int(row, "feedback_volume") for row in month_rows)
        month_summary[month_key]["rows"].extend(month_rows)

    monthly_trend = {
        month: {
            "feedback_volume": data["feedback_volume"],
            "avg_satisfaction": _weighted_average(data["rows"], "satisfaction_score"),
            "avg_friction": _weighted_average(data["rows"], "friction_score"),
        }
        for month, data in sorted(month_summary.items())
    }

    improvement_delta = 0.0
    if completed_delta_rows:
        total_completed_volume = sum(_int(row, "feedback_volume") for row in completed_delta_rows)
        improvement_delta = round(
            sum(row["delta"] * _int(row, "feedback_volume") for row in completed_delta_rows)
            / total_completed_volume,
            2,
        )

    return {
        "records": len(rows),
        "weighted_feedback_volume": total_volume,
        "customer_satisfaction_rate": round(satisfied_volume / total_volume, 3),
        "customer_satisfaction_rate_pct": round((satisfied_volume / total_volume) * 100, 1),
        "journey_friction_index": _weighted_average(rows, "friction_score"),
        "follow_up_completion_rate": round(len(follow_up_completed) / len(follow_up_required), 3),
        "follow_up_completion_rate_pct": round((len(follow_up_completed) / len(follow_up_required)) * 100, 1),
        "post_action_improvement_delta": improvement_delta,
        "at_risk_segment_count": len(at_risk_segments),
        "at_risk_segments": at_risk_segments,
        "segment_summary": segment_summary,
        "monthly_trend": monthly_trend,
    }


def main() -> None:
    summary = build_summary(load_rows(DATA_PATH))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
