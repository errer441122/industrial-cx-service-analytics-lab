# Influx Schema - Simulated Industrial CX Lab

This is a simulated design artifact. It is not connected to a real InfluxDB instance, company system, dealer system, production line, edge gateway, or telemetry source.

## Measurement

`industrial_service_telemetry`

## Tags

| Tag | Meaning |
| --- | --- |
| `asset_id` | Synthetic asset identifier such as `line-01-pump-01`. |

## Fields

| Field | Type | Meaning |
| --- | --- | --- |
| `rpm` | integer | Simulated rotational speed. |
| `temperature_c` | float | Simulated temperature in Celsius. |
| `vibration_mm_s` | float | Simulated vibration velocity. |
| `pressure_bar` | float | Simulated pressure. |
| `torque_nm` | float | Simulated torque. |
| `operating_hours` | float | Synthetic accumulated operating hours. |
| `error_code_count` | integer | Synthetic error count in the time window. |
| `service_delay_days` | integer | Synthetic after-sales/service delay proxy. |
| `anomaly_label` | integer | Controlled synthetic anomaly label. |
| `service_escalation_label` | integer | Controlled synthetic service-risk label. |

## Local Artifact

The local pipeline writes line protocol to:

```text
industrial-cx-ai-lab/artifacts/influx_line_protocol.txt
```

Reviewer boundary: this is schema and file evidence only. Do not present it as a real Influx deployment.
