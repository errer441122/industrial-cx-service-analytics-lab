# Reviewer SQL Module

This folder is the top-level shortcut for reviewers looking for SQL/DWH evidence.

The deeper project already contains SQL in:

- `production-sim-stack/sql/service_feature_mart.duckdb.sql`
- `industrial-cx-ai-lab/src/run_pipeline.py`, which writes a SQLite feature mart

`reviewer_service_mart.duckdb.sql` is a compact DuckDB mart that can be inspected without opening the full production simulation stack.

## Example

```bash
duckdb premium-mobility-brand_cx_review.duckdb < sql/reviewer_service_mart.duckdb.sql
```

It creates service-risk, anomaly-check, and line-summary views from the simulated industrial/CX dataset.
