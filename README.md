# Data Pipeline Project

This repository is a starter implementation of a secure, scalable data preparation pipeline for AE. It demonstrates a practical pattern for moving data from a source system into a warehouse, with an emphasis on orchestration, transformation, security, and governance.

## Project Goal

The project is designed to show how a team could build a production-ready pipeline that:
- ingests a file-based source from Azure Blob Storage,
- applies decryption, validation, and transformation steps,
- orchestrates the workflow with Airflow,
- models the data with dbt,
- loads the curated output into Snowflake for analytics and reporting.

## Architecture Overview

The current repository provides a lightweight scaffold for the full architecture. The design follows a standard batch-oriented data preparation flow that can be extended into a production platform.

### End-to-End Flow

1. A source file arrives in Azure Blob Storage.
2. A Python ingestion step downloads and validates the file.
3. Airflow orchestrates the workflow and handles retries and failure paths.
4. A transformation stage standardises the data and prepares it for modelling.
5. dbt creates curated models for downstream reporting.
6. Snowflake stores the final tables for analytics and business consumption.

### Raw Diagram

```text
+------------------------+
| Azure Blob Storage    |
| - incoming files      |
| - encrypted parquet   |
+-----------+------------+
            |
            v
+------------------------+
| Python Ingestion Layer|
| - download file       |
| - validate format     |
| - decrypt if required |
+-----------+------------+
            |
            v
+------------------------+
| Airflow Orchestration  |
| - DAG scheduling      |
| - retries / alerts    |
| - task dependencies   |
+-----------+------------+
            |
            v
+------------------------+
| Transformation Layer   |
| - schema mapping      |
| - data quality checks |
| - business rules      |
+-----------+------------+
            |
            v
+------------------------+
| dbt Models            |
| - staging             |
| - intermediate        |
| - marts               |
+-----------+------------+
            |
            v
+------------------------+
| Snowflake Warehouse   |
| - raw / curated tables|
| - analytics & reporting|
+------------------------+
```

### Component Responsibilities
- Azure Blob Storage: stores the incoming source files.
- Python: handles file download, preprocessing, and integration logic.
- Airflow: orchestrates job execution, retries, and scheduling.
- dbt: transforms raw inputs into curated models.
- Snowflake: serves as the analytics warehouse.

## Repository Structure

- data/ — sample source files for local testing, including CSVs, control files, and a Parquet sample
- src/pipeline/ — Python modules for ingestion and sample data loading
- airflow/dags/ — Airflow DAG skeleton for orchestration
- dbt/models/ — example dbt model structure
- docs/architecture.md — architecture notes and design rationale

## Getting Started

1. Create and activate a Python environment.
2. Install the dependencies:
   pip install -r requirements.txt
3. Copy .env.example to .env and populate the required values.
4. Run the sample loader locally:
   python3 src/pipeline/sample_source.py
5. Review the architecture notes in docs/architecture.md for the intended end-to-end design.

## Security and Governance

This project is structured around practical controls such as:
- secrets and credentials managed through environment variables or vault-backed services,
- TLS for data in transit,
- least-privilege access patterns for Snowflake roles,
- data quality checks and monitoring hooks for production readiness.

## Suggested Future Enhancements

The scaffold can be extended with:
- Azure Key Vault integration for secrets,
- decryption logic for encrypted files,
- Snowflake load tasks and schema management,
- dbt tests and documentation,
- alerting and observability for production operations.

## Data Preparation Focus Areas

This scaffold is intended to help you discuss:
- end-to-end architecture design,
- integration between Airflow, Python, dbt, and Snowflake,
- security boundaries and governance,
- operational considerations such as retries, observability, and schema evolution.
