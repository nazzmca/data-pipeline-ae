# Architecture Design

## End-to-End Flow

1. A file lands in Azure Blob Storage.
2. Airflow detects the arrival and starts the DAG.
3. A Python task downloads the encrypted Parquet file.
4. The file is decrypted using a key from Azure Key Vault.
5. A transformation step standardises the schema and applies masking rules.
6. dbt models prepare curated tables for analytics.
7. The final data is loaded into Snowflake.

## Component Responsibilities

- Azure Blob Storage: source storage for encrypted files.
- Airflow: orchestration, retries, and scheduling.
- Python: ingestion and transformation logic.
- dbt: transformation and data modelling.
- Snowflake: warehouse for analytics and reporting.

## Security Controls

- TLS for transport between Azure, Airflow, and Snowflake.
- Secrets stored in Azure Key Vault.
- Snowflake RBAC with roles such as `loader`, `transformer`, and `analyst`.
- Data masking and least-privilege access for sensitive customer data.

## Operational Considerations

- Add monitoring to track DAG failures, row counts, and freshness.
- Use unit tests and dbt tests for schema and data quality.
- Implement backfills and idempotent loads using write-ahead patterns.
- Introduce alerting for failed loads or unexpected schema changes.
