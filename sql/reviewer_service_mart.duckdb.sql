CREATE OR REPLACE TABLE stg_opcua_service_events AS
SELECT *
FROM read_csv_auto('industrial-cx-ai-lab/data/opcua_service_events.csv', HEADER = TRUE);

CREATE OR REPLACE VIEW mart_service_risk AS
SELECT
  event_id,
  bike_family,
  region,
  opcua_node,
  vibration_rms,
  temperature_c,
  battery_voltage,
  oil_pressure_bar,
  service_delay_days,
  nps,
  warranty_claims,
  telemetry_dropouts,
  churn_risk,
  ROUND(
    vibration_rms * 0.18
    + temperature_c * 0.025
    + service_delay_days * 0.08
    + warranty_claims * 0.8
    + telemetry_dropouts * 0.7
    - nps * 0.12
    - oil_pressure_bar * 0.25,
    3
  ) AS service_risk_index,
  CASE
    WHEN churn_risk = 1 THEN 'human_service_review'
    WHEN vibration_rms >= 4.5 OR temperature_c >= 92 OR telemetry_dropouts >= 1 THEN 'monitor_industrial_signal'
    ELSE 'standard_follow_up'
  END AS reviewer_decision_band
FROM stg_opcua_service_events;

CREATE OR REPLACE VIEW dq_anomaly_checks AS
SELECT
  event_id,
  bike_family,
  region,
  CASE WHEN vibration_rms >= 4.5 THEN 1 ELSE 0 END AS vibration_anomaly,
  CASE WHEN temperature_c >= 92 THEN 1 ELSE 0 END AS temperature_anomaly,
  CASE WHEN oil_pressure_bar <= 2.1 THEN 1 ELSE 0 END AS oil_pressure_anomaly,
  CASE WHEN telemetry_dropouts >= 1 THEN 1 ELSE 0 END AS telemetry_gap
FROM stg_opcua_service_events;

CREATE OR REPLACE VIEW reporting_family_summary AS
SELECT
  bike_family,
  COUNT(*) AS event_count,
  ROUND(AVG(service_risk_index), 3) AS avg_service_risk_index,
  SUM(churn_risk) AS human_review_queue,
  SUM(CASE WHEN reviewer_decision_band = 'monitor_industrial_signal' THEN 1 ELSE 0 END) AS monitoring_queue
FROM mart_service_risk
GROUP BY bike_family
ORDER BY avg_service_risk_index DESC;
