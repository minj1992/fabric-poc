# 📡 Alerting & Monitoring Design

## 1. Pipeline Failure Detection
- **Mechanism**: Data Factory Pipeline Alert rules.
- **Trigger**: PipelineRunStatus == Failed.
- **Action Group**: Email notification to Dev / Ops team.

## 2. Data Quality Failure Logging
- **Mechanism**: `data_quality_results` table monitoring.
- **Action**: Daily report sent via Power BI or logic app for any status 'Fail'.

## 3. SLA Monitoring Logic
- **Check**: Compare `end_time - start_time` against `expected_sla_time` in `pipeline_metadata`.
- **Threshold**: Breach alert if actual > expected.

## 4. Capacity Monitoring
- **Tools**: Fabric Capacity Metrics App.
- **Metric**: CU (Capacity Unit) consumption.

## 5. Alert Integration via Azure Monitor
- Configure Diagnostic Settings to send logs to Log Analytics workspace.
- KQL Query to monitor errors:
```kusto
FabricPipelineRuns
| where Status == "Failed"
| project PipelineName, RunId, StartTime, ErrorMessage
```
