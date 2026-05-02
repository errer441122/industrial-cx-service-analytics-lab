-- DuckDB/dbt-style feature mart sketch for the industrial production simulation stack.
-- Run from production-sim-stack when DuckDB is installed:
-- duckdb artifacts/industrial_service_mart.duckdb < sql/service_feature_mart.duckdb.sql

CREATE OR REPLACE TABLE raw_iot_stream AS
SELECT *
FROM read_csv_auto('data/iot_stream_seed.csv', HEADER = TRUE);

CREATE OR REPLACE TABLE industrial_service_feature_mart AS
SELECT
    event_id,
    line,
    asset_family,
    timestamp,
    opcua_node,
    vibration_rms,
    temperature_c,
    battery_voltage,
    oil_pressure_bar,
    service_delay_days,
    nps,
    warranty_claims,
    telemetry_dropouts,
    CASE WHEN vibration_rms >= 4.5 THEN 1 ELSE 0 END AS high_vibration_flag,
    CASE WHEN temperature_c >= 92 THEN 1 ELSE 0 END AS high_temperature_flag,
    CASE WHEN oil_pressure_bar <= 2.0 THEN 1 ELSE 0 END AS low_oil_pressure_flag,
    CASE WHEN service_delay_days >= 15 THEN 1 ELSE 0 END AS delayed_service_flag,
    service_escalation
FROM raw_iot_stream;
