import logging
import datetime

class FabricLogger:
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.logger = logging.getLogger(pipeline_name)
        self.logger.setLevel(logging.INFO)
        
        # Configure standard output logging
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def log_start(self, run_id):
        self.logger.info(f"Pipeline {self.pipeline_name} started with Run ID: {run_id}")
        
    def log_success(self, run_id, records_processed):
        self.logger.info(f"Pipeline {self.pipeline_name} succeeded. Records processed: {records_processed}")
        
    def log_error(self, run_id, error_message):
        self.logger.error(f"Pipeline {self.pipeline_name} failed. Error: {error_message}")

# Example usage in a notebook:
# logger = FabricLogger("SalesPipeline")
# logger.log_start(mssparkutils.runtime.getContext().get('jobId'))
