# 🚀 Enterprise Microsoft Fabric Automation Lab

## 🎯 Objective

Build an enterprise-grade Microsoft Fabric data platform lab using:

- Azure DevOps (Git-based source control)
- Microsoft Fabric Workspace
- Lakehouse Architecture
- Metadata-driven pipelines
- Enterprise monitoring & alerting
- CI/CD-ready structure

This lab simulates a production-ready architecture.

---

# 🏗 ARCHITECTURE OVERVIEW

Fabric Workspace → Lakehouse → Notebooks/Pipelines → Azure DevOps Repo (Sync)

We will:

1. Manually create Fabric Workspace & Lakehouse
2. Create Notebooks & Pipelines inside the Fabric UI
3. Connect the Workspace to Azure DevOps
4. Commit artifacts from Fabric to Git (Baseline)
5. Use VS Code for advanced metadata & monitoring code refinement
6. Implement CI/CD via REST APIs (Advanced Automation)

---

# 📁 REPOSITORY STRUCTURE TO GENERATE

Create the following folder structure:

enterprise-fabric-lab/
│
├── notebooks/
│   ├── 01_create_metadata_tables.ipynb
│   ├── 02_load_raw_to_silver.ipynb
│   ├── 03_data_quality_checks.ipynb
│   └── 04_audit_logging.ipynb
│
├── sql/
│   ├── create_metadata_tables.sql
│   ├── create_audit_tables.sql
│   └── create_data_quality_tables.sql
│
├── pipelines/
│   └── sales_pipeline_definition.json
│
├── monitoring/
│   ├── logging_framework.py
│   └── alerting_design.md
│
└── enterprise-fabric-lab-plan.md

---

# 🧠 METADATA FRAMEWORK DESIGN

Create metadata table definition:

pipeline_metadata:
- source_name STRING
- source_path STRING
- target_table STRING
- load_type STRING
- watermark_column STRING
- expected_sla_time STRING
- is_active BOOLEAN

audit_pipeline_runs:
- pipeline_name STRING
- run_id STRING
- start_time TIMESTAMP
- end_time TIMESTAMP
- status STRING
- records_processed INT
- error_message STRING

data_quality_results:
- table_name STRING
- check_name STRING
- check_status STRING
- check_time TIMESTAMP

---

# 📊 NOTEBOOK REQUIREMENTS

01_create_metadata_tables.ipynb
- Create metadata tables
- Insert sample metadata
- Create audit & DQ tables

02_load_raw_to_silver.ipynb
- Read metadata
- Loop through active sources
- Read CSV from Lakehouse Files/raw
- Write Delta table to Lakehouse Tables
- Log run to audit table

03_data_quality_checks.ipynb
- Validate:
    - No empty dataset
    - No negative amounts
    - Record count > 0
- Write results to data_quality_results

04_audit_logging.ipynb
- Wrap logic in try/except
- Capture:
    - start_time
    - end_time
    - status
    - error_message

---

# 📡 MONITORING & ALERT STRATEGY

Implement:

1. Pipeline failure detection
2. Data quality failure logging
3. SLA monitoring logic
4. Capacity monitoring design (documentation)
5. Alert integration design via Azure Monitor

---

# 🔐 SECURITY DESIGN

Include:

- RBAC model:
    - Admin
    - Developer
    - Viewer
- Service principal authentication model
- Git branch strategy
- Dev / UAT / Prod workspace strategy

---

# 🛠 MANUAL STEPS TO EXECUTE LAB

## STEP 1 — Fabric Workspace Setup (Manual)

1. Create Workspace: `Enterprise-Dev`
2. Assign Capacity
3. Create Lakehouse: `EnterpriseLakehouse`
4. Upload sample CSV to `Files/raw/sales.csv`

## STEP 2 — Artifact Creation (Manual)

1. Create Notebooks (01 to 04) within Fabric UI.
2. Copy the logic from the local `notebooks/` folder into Fabric Notebooks.
3. Create Data Pipeline manually.

## STEP 3 — Git Integration & Baseline Sync

1. Open Workspace Settings.
2. Connect to Azure DevOps (Empty Repo).
3. Select repo and `main` branch.
4. Click **Sync/Commit** from Fabric to push artifacts to Git.
5. Verify Git now contains `.item` folders and `item.config.json` files.

---

## STEP 4 — Run Setup Notebook

Run:
01_create_metadata_tables.ipynb

Verify:
- Metadata tables created
- Audit tables created
- DQ tables created

---

## STEP 5 — Create Pipeline (Manual)

1. Create new Data Pipeline
2. Add Notebook activity:
   - 02_load_raw_to_silver
3. Add Notebook activity:
   - 03_data_quality_checks
4. Add Notebook activity:
   - 04_audit_logging
5. Attach Lakehouse
6. Save pipeline

---

## STEP 6 — Advanced Automation: API-Based Deployment

If you want to achieve **Git-first** automation, follow these steps:

1. **Service Principal Setup**:
   - Register an App in Microsoft Entra ID.
   - Grant `Workspace.ReadWrite.All` or specific workspace permissions.
   - Add the Service Principal to the Fabric Workspace as a 'Contributor' or 'Admin'.

2. **Artifact Definition**:
   - For Notebooks: Use the Fabric REST API `POST /v1/workspaces/{workspaceId}/items` with `type: "Notebook"`.
   - The payload must contain the base64 encoded `.ipynb` content in the `parts` section of the multipart request or use the payload schema for notebooks.

3. **Python Deployment Script**:
   - Use `msal` for authentication.
   - Use `requests` to call the Fabric REST API.
   - Automate the creation of Notebooks and Pipelines directly from the local `notebooks/` and `pipelines/` directories.

4. **CI/CD Pipeline**:
   - Configure an Azure DevOps Pipeline.
   - Trigger: Push to `main`.
   - Action: Run the Python deployment script to sync local files to the Fabric Workspace.

---

## STEP 7 — Monitoring Setup (Enterprise Simulation)

1. Enable Diagnostic Logs
2. Send logs to Log Analytics
3. Create alert rule:
   Condition: PipelineRunStatus == Failed
4. Configure email action group

---

# 📈 ENTERPRISE EXTENSIONS (OPTIONAL)

- Implement CI/CD promotion strategy
- Implement Dev/UAT/Prod branching
- Automate workspace provisioning via REST API
- Implement SLA breach detection
- Create Power BI dashboard for monitoring

---

# 🎯 EXPECTED OUTCOME

By completing this lab, you will understand:

- GitOps model in Fabric
- Metadata-driven architecture
- Enterprise monitoring design
- Audit logging framework
- Data quality framework
- CI/CD-ready structure
- Automation possibilities

---

END OF LAB PLAN