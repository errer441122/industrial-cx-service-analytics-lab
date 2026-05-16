CREATE OR REPLACE VIEW cx_feedback_base AS
SELECT
    feedback_id,
    CAST(date AS DATE) AS feedback_date,
    channel,
    segment,
    journey_stage,
    region,
    CAST(satisfaction_score AS INTEGER) AS satisfaction_score,
    CAST(feedback_volume AS INTEGER) AS feedback_volume,
    issue_category,
    CAST(friction_score AS INTEGER) AS friction_score,
    follow_up_required,
    follow_up_completed,
    CAST(post_action_score AS INTEGER) AS post_action_score,
    comment
FROM read_csv_auto('cx-analyst-lab/data/cx_feedback_sample.csv', HEADER = TRUE);

CREATE OR REPLACE VIEW cx_satisfaction_by_segment AS
SELECT
    segment,
    SUM(feedback_volume) AS weighted_feedback_volume,
    ROUND(SUM(CASE WHEN satisfaction_score >= 4 THEN feedback_volume ELSE 0 END) * 100.0 / SUM(feedback_volume), 1) AS customer_satisfaction_rate_pct,
    ROUND(SUM(satisfaction_score * feedback_volume) * 1.0 / SUM(feedback_volume), 2) AS weighted_avg_satisfaction,
    ROUND(SUM(friction_score * feedback_volume) * 1.0 / SUM(feedback_volume), 2) AS journey_friction_index
FROM cx_feedback_base
GROUP BY segment;

CREATE OR REPLACE VIEW cx_journey_friction AS
SELECT
    journey_stage,
    issue_category,
    SUM(feedback_volume) AS weighted_feedback_volume,
    ROUND(SUM(friction_score * feedback_volume) * 1.0 / SUM(feedback_volume), 2) AS journey_friction_index,
    COUNT(*) AS feedback_records
FROM cx_feedback_base
GROUP BY journey_stage, issue_category;

CREATE OR REPLACE VIEW cx_follow_up_tracker AS
SELECT
    segment,
    journey_stage,
    SUM(CASE WHEN follow_up_required = 'yes' THEN 1 ELSE 0 END) AS required_follow_ups,
    SUM(CASE WHEN follow_up_completed = 'yes' THEN 1 ELSE 0 END) AS completed_follow_ups,
    ROUND(
        SUM(CASE WHEN follow_up_completed = 'yes' THEN 1 ELSE 0 END) * 100.0
        / NULLIF(SUM(CASE WHEN follow_up_required = 'yes' THEN 1 ELSE 0 END), 0),
        1
    ) AS follow_up_completion_rate_pct,
    ROUND(AVG(CASE WHEN follow_up_completed = 'yes' THEN post_action_score - satisfaction_score END), 2) AS post_action_improvement_delta
FROM cx_feedback_base
GROUP BY segment, journey_stage;
