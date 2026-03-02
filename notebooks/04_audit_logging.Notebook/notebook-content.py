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

from pyspark.sql.functions import current_timestamp

# Sample audit logging notebook logic
try:
    # Core processing logic goes here
    print("Starting core processing...")
    
    # Simulate processing
    spark.sql("SELECT current_timestamp() as start_time").show()
    
    # Capture run details
    pipeline_name = "SalesPipeline"
    run_id = mssparkutils.runtime.getContext().get('jobId')
    status = "Success"
    error_message = None
    
    print(f"Pipeline {pipeline_name} with run_id {run_id} completed successfully.")
    
    # Final audit log entry
    spark.sql(f"""
    INSERT INTO audit_pipeline_runs VALUES 
    ('{pipeline_name}', '{run_id}', current_timestamp(), current_timestamp(), '{status}', 1, '{error_message}')
    """)
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
    # Log error
    spark.sql(f"""
    INSERT INTO audit_pipeline_runs VALUES 
    ('{pipeline_name}', '{run_id}', current_timestamp(), current_timestamp(), 'Failed', 0, '{str(e)}')
    """)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
