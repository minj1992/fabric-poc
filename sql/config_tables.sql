-- config_environment
CREATE TABLE IF NOT EXISTS config_environment (
    environment STRING,
    storage_path STRING,
    notification_email STRING
) USING DELTA;

-- config_ingestion_metadata
CREATE TABLE IF NOT EXISTS config_ingestion_metadata (
    source_id STRING,
    domain STRING,
    source_object STRING,
    target_lakehouse STRING,
    target_table STRING,
    file_format STRING,
    load_type STRING,
    watermark_column STRING,
    primary_key STRING,
    active_flag BOOLEAN,
    created_date TIMESTAMP
) USING DELTA;

-- platform_error_log
CREATE TABLE IF NOT EXISTS platform_error_log (
    layer STRING,
    table_name STRING,
    error_message STRING,
    error_timestamp TIMESTAMP
) USING DELTA;

-- Insert Sample Metadata
INSERT INTO config_ingestion_metadata VALUES 
('CL001', 'Claims', 'claims_sample.csv', 'LH_Claims', 'claims_bronze', 'csv', 'full', 'none', 'claim_id', true, current_timestamp());
