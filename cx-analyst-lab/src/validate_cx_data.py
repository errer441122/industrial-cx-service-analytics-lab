from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cx_feedback_sample.csv"
REQUIRED_FIELDS = {
    "feedback_id",
    "date",
    "channel",
    "segment",
    "journey_stage",
    "region",
    "satisfaction_score",
    "feedback_volume",
    "issue_category",
    "friction_score",
    "follow_up_required",
    "follow_up_completed",
    "post_action_score",
    "comment",
}
YES_NO = {"yes", "no"}


def load_rows(path: Path = DATA_PATH) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_FIELDS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required fields: {sorted(missing)}")
        return list(reader)


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()

    for index, row in enumerate(rows, start=2):
        feedback_id = row["feedback_id"].strip()
        if not feedback_id:
            errors.append(f"line {index}: feedback_id is required")
        if feedback_id in seen_ids:
            errors.append(f"line {index}: duplicate feedback_id {feedback_id}")
        seen_ids.add(feedback_id)

        try:
            datetime.strptime(row["date"], "%Y-%m-%d")
        except ValueError:
            errors.append(f"line {index}: date must be YYYY-MM-DD")

        for field in ("channel", "segment", "journey_stage", "region", "issue_category", "comment"):
            if not row[field].strip():
                errors.append(f"line {index}: {field} is required")

        for field in ("satisfaction_score", "friction_score", "post_action_score"):
            try:
                value = int(row[field])
            except ValueError:
                errors.append(f"line {index}: {field} must be an integer")
                continue
            if value < 1 or value > 5:
                errors.append(f"line {index}: {field} must be between 1 and 5")

        try:
            volume = int(row["feedback_volume"])
        except ValueError:
            errors.append(f"line {index}: feedback_volume must be an integer")
        else:
            if volume <= 0:
                errors.append(f"line {index}: feedback_volume must be positive")

        required = row["follow_up_required"].strip().lower()
        completed = row["follow_up_completed"].strip().lower()
        if required not in YES_NO:
            errors.append(f"line {index}: follow_up_required must be yes or no")
        if completed not in YES_NO:
            errors.append(f"line {index}: follow_up_completed must be yes or no")
        if required == "no" and completed == "yes":
            errors.append(f"line {index}: follow_up_completed cannot be yes when follow_up_required is no")

    if len(rows) < 10:
        errors.append("dataset must contain at least 10 feedback records")

    return errors


def validate_file(path: Path = DATA_PATH) -> list[str]:
    return validate_rows(load_rows(path))


def main() -> None:
    errors = validate_file()
    if errors:
        raise SystemExit("CX data validation failed:\n- " + "\n- ".join(errors))
    print("CX data validation passed.")


if __name__ == "__main__":
    main()
