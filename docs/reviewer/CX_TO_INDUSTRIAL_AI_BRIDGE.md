# CX To Industrial AI Bridge

The repository keeps the original CX workbook visible while adding an industrial AI supplement. The bridge is the service experience: customer pain often appears as delays, repeat contacts, unresolved service issues, or quality concerns, while industrial telemetry can expose operating conditions that may explain or prioritize those issues.

## Bridge Logic

| Layer | Signal | Repository evidence |
| --- | --- | --- |
| Customer experience | satisfaction, journey friction, service delay, action ownership | workbook, `cx-data.js`, `cx-analyst-lab/` |
| Industrial telemetry | temperature, vibration, pressure, torque, operating hours, error codes | `industrial-cx-ai-lab/data/simulated_telemetry.csv` |
| Service-risk scoring | anomaly context plus delay and satisfaction proxy | `industrial-cx-ai-lab/src/service_risk_model.py` |
| Monitoring | line protocol and dashboard design | `industrial-cx-ai-lab/artifacts/influx_line_protocol.txt`, `ops/grafana_dashboard.json` |
| Operating process | human review and maintenance policy note | `industrial-cx-ai-lab/artifacts/maintenance_policy_note.md` |

## Human Review Boundary

The model can help rank records for review. It cannot decide customer treatment, warranty action, safety action, dealer assessment, or maintenance execution. Any real use would require approved data, validated labels, domain experts, safety review, and documented escalation procedures.
