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

from pyspark.sql.functions import current_timestamp, lit

# Read active metadata sources
metadata_df = spark.sql("SELECT * FROM pipeline_metadata WHERE is_active = true")
sources = metadata_df.collect()

for source in sources:
    source_name = source['source_name']
    source_path = source['source_path']
    target_table = source['target_table']
    
    print(f"Processing: {source_name} from {source_path} into {target_table}")
    
    try:
        # Load raw CSV
        df = spark.read.option("header", "true").csv(f"Files/raw/{source_name}.csv")
        
        # Basic transformations: add load_timestamp
        df_silver = df.withColumn("load_timestamp", current_timestamp())
        
        # Write to Delta table
        df_silver.write.format("delta").mode("overwrite").saveAsTable(target_table)
        
        # Log Success to Audit
        spark.sql(f"""
        INSERT INTO audit_pipeline_runs VALUES 
        ('{source_name}', '{mssparkutils.runtime.getContext().get('jobId')}', current_timestamp(), current_timestamp(), 'Success', {df_silver.count()}, NULL)
        """)
        
    except Exception as e:
        print(f"Error processing {source_name}: {str(e)}")
        # Log Failure to Audit
        spark.sql(f"""
        INSERT INTO audit_pipeline_runs VALUES 
        ('{source_name}', '{mssparkutils.runtime.getContext().get('jobId')}', current_timestamp(), current_timestamp(), 'Failed', 0, '{str(e)}')
        """)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
