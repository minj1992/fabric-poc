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

from pyspark.sql.functions import current_timestamp, col

# Read active metadata sources
metadata_df = spark.sql("SELECT * FROM pipeline_metadata WHERE is_active = true")
sources = metadata_df.collect()

for source in sources:
    target_table = source['target_table']
    
    print(f"Performing DQ checks on: {target_table}")
    
    df = spark.table(target_table)
    
    # DQ Check 1: Record count > 0
    count = df.count()
    check1_status = 'Pass' if count > 0 else 'Fail'
    spark.sql(f"INSERT INTO data_quality_results VALUES ('{target_table}', 'record_count_gt_0', '{check1_status}', current_timestamp())")
    
    # DQ Check 2: No empty dataset
    check2_status = 'Pass' if count > 0 else 'Fail'
    spark.sql(f"INSERT INTO data_quality_results VALUES ('{target_table}', 'no_empty_dataset', '{check2_status}', current_timestamp())")
    
    # DQ Check 3: No negative amounts (assuming an 'amount' column exists for demonstration)
    try:
        neg_count = df.filter(col("amount") < 0).count()
        check3_status = 'Pass' if neg_count == 0 else 'Fail'
    except:
        check3_status = 'Skipped' # 'amount' column may not exist
        
    spark.sql(f"INSERT INTO data_quality_results VALUES ('{target_table}', 'no_negative_amounts', '{check3_status}', current_timestamp())")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
