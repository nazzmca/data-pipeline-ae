# Data Pipeline Project: User Guide

This guide walks you through the data pipeline project, explaining its purpose, structure, and how to work with it.

## Project Overview

This is a starter implementation of a secure, scalable data preparation pipeline for AE. It demonstrates how to move data from a source system (Azure Blob Storage) through orchestration, transformation, and finally into a warehouse (Snowflake) for reporting and analytics.

The project is designed around realistic data engineering patterns and includes sample data, transformation logic, and security-focused output handling.

## Key Components

### 1. Data Ingestion Layer
**Location**: `src/pipeline/`

This layer handles fetching data from source systems.

- **ingest.py**: Downloads encrypted files from Azure Blob Storage
- **sample_source.py**: Loads sample data locally for testing and development

**How it works**:
- The loader scans the `data/` folder for Parquet files
- Each Parquet file has a matching control file (`.parquet.ctrl.csv`)
- The control file contains metadata: business date and expected record count
- The loader validates and returns this metadata alongside the data

**Example usage**:
```python
from src.pipeline.sample_source import load_sample_dataset

datasets = load_sample_dataset()
for dataset in datasets:
    print(f"File: {dataset['data_file'].name}")
    print(f"Business Date: {dataset['business_date']}")
    print(f"Record Count: {dataset['record_count']}")
```

### 2. Data Files
**Location**: `data/`

The project includes two types of sample data:

**Parquet files** (main pipeline):
- `customers.parquet` — customer records
- `orders.parquet` — order transactions
- `products.parquet` — product catalog

Each Parquet file has a matching control file with metadata.

**CSV files** (reference examples):
- Located in `data/csv/` subfolder
- Same data as Parquet but in CSV format
- Useful for testing alternative ingestion methods

### 3. Orchestration Layer
**Location**: `airflow/dags/`

Airflow manages the workflow and scheduling.

- **azure_to_snowflake_dag.py**: Skeleton DAG that shows the pipeline structure
- Defines task dependencies and retry logic
- Currently a placeholder ready for production implementation

### 4. Transformation Layer
**Location**: `dbt/models/`

dbt handles data modeling and transformations.

#### Model Hierarchy

```
Raw Data (Parquet files)
    ↓
stg_customers.sql (Staging)
    ↓
int_customer_orders.sql (Intermediate - Joins)
    ↓
mart_customer_summary.sql (Mart - Final Output with Masking)
    ↓
security_check.sql (Validation - Safe Fields Only)
```

#### Each Model's Purpose

1. **stg_customers.sql** (Staging)
   - Cleans and standardizes customer data
   - Casts data types (e.g., customer_id to integer)
   - Adds a load timestamp

2. **int_customer_orders.sql** (Intermediate)
   - Joins customers with their orders
   - Calculates aggregations: total order value, order count
   - Groups by customer

3. **mart_customer_summary.sql** (Mart Output)
   - Produces the final reporting table
   - **Masks sensitive data**: email addresses are masked to `@masked.example`
   - Ready for analytics and reporting consumption

4. **security_check.sql** (Security Validation)
   - Lightweight output validation
   - Filters to safe, non-sensitive fields only
   - Ensures masking was applied correctly

### 5. Configuration
**Location**: `.env.example`

Contains environment variables for:
- Azure Blob Storage credentials
- Snowflake connection details
- Key Vault references for secrets

Copy to `.env` and fill in your actual values.

## Data Flow (End-to-End)

```
1. Data Lands in Azure Blob Storage
   ↓
2. Python Ingestion Layer (src/pipeline/ingest.py)
   - Downloads encrypted Parquet file
   - Validates control metadata
   ↓
3. Airflow Orchestration (airflow/dags/)
   - Schedules and monitors execution
   - Handles retries and failure paths
   ↓
4. dbt Transformations (dbt/models/)
   - Staging: clean and standardize
   - Intermediate: join and aggregate
   - Mart: apply masking rules
   - Security Check: validate output
   ↓
5. Snowflake Warehouse
   - Final tables stored
   - Ready for analytics and reporting
```

## How to Use the Project

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Azure and Snowflake credentials
   ```

### Load Sample Data Locally

```bash
python3 src/pipeline/sample_source.py
```

Output shows:
- File names (e.g., `customers.parquet`)
- Business dates from control files
- Record counts for validation

### Run Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

This validates that the sample loader correctly reads the Parquet files and their metadata.

### Inspect dbt Models

Review the transformation logic in `dbt/models/`:
- Each `.sql` file is a model
- Models reference each other using `{{ ref() }}`
- The hierarchy follows staging → intermediate → mart → check pattern

## Security & Governance Highlights

### Data Masking
- Email addresses are masked in the mart layer
- Pattern: `name@domain.com` → `name@masked.example`
- Sensitive data never reaches reporting consumers

### Role-Based Access Control (RBAC)
Plan for Snowflake:
- **loader**: Can insert into raw tables
- **transformer**: Can create intermediate and mart tables
- **analyst**: Can read from mart and security_check views only

### Control Files
- Every data file has a `.ctrl.csv` sibling
- Contains: filename, business_date, record_count
- Allows validation: "Does the file have the expected row count?"

### Data Lineage
- dbt models track data lineage automatically
- Each row in the mart can trace back to its source

## Common Workflows

### Scenario: Update Customer Logic

1. Edit `dbt/models/stg_customers.sql`
2. Add new transformations (e.g., segment calculation)
3. dbt automatically propagates changes downstream
4. Security check ensures masking still applies

### Scenario: Add a New Data Source

1. Add Parquet file to `data/` folder
2. Create matching `.parquet.ctrl.csv` control file
3. Create a new staging model: `stg_[source].sql`
4. Reference it in intermediate models as needed

### Scenario: Validate Output

1. Run `security_check.sql` to ensure masking was applied
2. Count records: should match control file metadata
3. Spot-check masked values: should show `@masked.example`

## File Structure Summary

```
.
├── README.md                          # Project overview
├── GUIDE.md                           # This file
├── .env.example                       # Environment template
├── requirements.txt                   # Python dependencies
├── data/
│   ├── customers.parquet              # Sample customer data
│   ├── customers.parquet.ctrl.csv     # Metadata: date, count
│   ├── orders.parquet
│   ├── orders.parquet.ctrl.csv
│   ├── products.parquet
│   ├── products.parquet.ctrl.csv
│   └── csv/                           # CSV examples subfolder
│       ├── sample_customers.csv
│       ├── sample_orders.csv
│       └── ...
├── src/
│   └── pipeline/
│       ├── ingest.py                  # Azure ingestion logic
│       └── sample_source.py           # Local sample loader
├── airflow/
│   └── dags/
│       └── azure_to_snowflake_dag.py  # Orchestration skeleton
├── dbt/
│   └── models/
│       ├── stg_customers.sql          # Staging
│       ├── int_customer_orders.sql    # Intermediate join
│       ├── mart_customer_summary.sql  # Final output + masking
│       └── security_check.sql         # Validation view
├── docs/
│   └── architecture.md                # Architecture notes
└── tests/
    └── test_sample_source.py          # Unit tests
```

## Next Steps for Production

1. **Implement Snowflake loads**: Replace dbt skeleton with actual warehouse schema
2. **Add decryption**: Implement decryption logic in the ingestion layer
3. **Enable Azure Key Vault**: Store secrets and encryption keys securely
4. **Add monitoring**: Track DAG execution, data freshness, quality metrics
5. **Expand dbt tests**: Add data quality checks (nulls, duplicates, ranges)
6. **Implement alerting**: Send alerts for failures or SLA breaches

## Key Takeaways

- **Modular design**: Each layer (ingest, transform, output) is independent
- **Security-first**: Masking and RBAC built in from the start
- **Control files**: Enable validation and metadata tracking
- **Reusable patterns**: dbt staging → intermediate → mart flow is production-ready
- **Sample data**: Makes local development and testing easy

## Questions?

Review the individual files for deeper understanding:
- `README.md` — Quick start
- `docs/architecture.md` — Architecture decisions
- `tests/test_sample_source.py` — How the loader works
- `dbt/models/*.sql` — Transformation logic in detail
