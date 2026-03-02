# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "aa83b357-508a-40bb-9f83-295ad2dd17f4",
# META       "default_lakehouse_name": "EnterpriseLakehouse",
# META       "default_lakehouse_workspace_id": "2dc4a7ef-58a8-43b5-91b2-02ade4ab7583",
# META       "known_lakehouses": [
# META         {
# META           "id": "aa83b357-508a-40bb-9f83-295ad2dd17f4"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.types import *
from pyspark.sql.functions import current_timestamp

# Create Pipeline Metadata Table
spark.sql("""
CREATE TABLE IF NOT EXISTS pipeline_metadata (
    source_name STRING,
    source_path STRING,
    target_table STRING,
    load_type STRING,
    watermark_column STRING,
    expected_sla_time STRING,
    is_active BOOLEAN
)
""")

# Insert Sample Metadata
spark.sql("""
INSERT INTO pipeline_metadata VALUES 
('sales_raw', 'Files/raw/sales.csv', 'sales_silver', 'full_load', 'none', '02:00:00', true)
""")

# Create Audit Pipeline Runs Table
spark.sql("""
CREATE TABLE IF NOT EXISTS audit_pipeline_runs (
    pipeline_name STRING,
    run_id STRING,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status STRING,
    records_processed INT,
    error_message STRING
)
""")

# Create Data Quality Results Table
spark.sql("""
CREATE TABLE IF NOT EXISTS data_quality_results (
    table_name STRING,
    check_name STRING,
    check_status STRING,
    check_time TIMESTAMP
)
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
