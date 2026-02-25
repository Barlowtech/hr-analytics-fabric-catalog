# HR Analytics Fabric Catalog - Research Notes

This document summarizes all patterns found in the catalog, organized by domain.
This is a reference document for understanding the breadth of the catalog and quick lookups.

---

## Data Organization and Structuring (Domain 1)

**Total Patterns:** 6

### Medallion Architecture (Bronze-Silver-Gold)
- **Complexity:** High
- **Maturity:** GA
- **Summary:** Implements a three-layer medallion architecture (Bronze, Silver, Gold) for progressive data refinement in OneLake.

### Delta Lake Partitioning Strategy
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Partitions Delta tables by business dimensions to optimize query performance and reduce scan costs.

### Lakehouse vs Warehouse Selection
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Decision framework for choosing between Lakehouse and Warehouse based on workload characteristics.

### OneLake Shortcuts for Data Sharing
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** Uses OneLake shortcuts as virtual references to data elsewhere without copying.

### Direct Lake Semantic Model
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Creates semantic models that directly reference OneLake Delta tables in Direct Lake mode for real-time analytics.

### Hub-and-Spoke Workspace Design
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Hub workspace contains shared reference data; spoke workspaces (HR, Recruiting, Finance) build domain-specific analytics.

---

## Transformation and Processing (Domain 2)

**Total Patterns:** 13

### Spark Notebook ETL Pipelines
- **Complexity:** High
- **Maturity:** GA
- **Summary:** PySpark notebooks for complex Bronze-to-Silver and Silver-to-Gold transformations with full programming power.

### Dataflow Gen2 Low-Code Transformations
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** Power Query Online visual ETL for simple-to-moderate transformations without coding.

### Incremental Loading with Watermarks
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Captures only new/modified records since last run using watermark columns to reduce refresh time.

### Slowly Changing Dimensions Type 2
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Maintains historical versions with validity dates enabling time-travel analysis of attribute changes.

### Change Data Capture (CDC) for Auditing
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Records before/after values of all modifications with user and timestamp for compliance audit trails.

### dbt Integration for Data Transformation
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** SQL-based dbt models with version control, testing, documentation enabling software engineering discipline.

### Data Quality Validation Framework
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Automated checks after ETL for anomalies, nulls, schema violations, business rule violations preventing bad data propagation.

### PII Tokenization and Pseudonymization
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Replaces Personally Identifiable Information (PII) with deterministic tokens using Microsoft Presidio and PySpark, enabling data sharing and analytics without exposing actual personal data.

### Automated Data Retention and Purge Pipeline
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Implements scheduled automated pipelines that evaluate data age against retention rules, execute secure deletion with audit trails, and support legal hold overrides for compliance.

### Dual-Approval Change Management Pipeline
- **Complexity:** Medium
- **Maturity:** Emerging
- **Summary:** Enforces dual-approval (business and governance) before production pipeline deployment, implementing four-eyes principle via Azure DevOps gates.

### PII Tokenization and Pseudonymization
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Replaces Personally Identifiable Information (PII) with deterministic tokens using Microsoft Presidio and PySpark, enabling data sharing and analytics without exposing actual personal data.

### Automated Data Retention and Purge Pipeline
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Implements scheduled automated pipelines that evaluate data age against retention rules, execute secure deletion with audit trails, and support legal hold overrides for compliance.

### Dual-Approval Change Management Pipeline
- **Complexity:** Medium
- **Maturity:** Emerging
- **Summary:** Enforces dual-approval (business and governance) before production pipeline deployment, implementing four-eyes principle via Azure DevOps gates.

---

## Governance and Security (Domain 3)

**Total Patterns:** 20

### Microsoft Purview Data Map
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Creates comprehensive data catalog in Purview mapping all assets, lineage, classifications, and sensitive data locations.

### Sensitivity Labels for Data Classification
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Applies sensitivity labels (Highly Confidential, Confidential, Internal) to tables and columns triggering data masking and access controls.

### Row-Level Security (RLS) at Gold Layer
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Restricts query results based on user identity/role so managers see only their team's data and employees see personal data.

### Dynamic Data Masking for Development/Test
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Masks sensitive data values in non-production environments so developers see realistic data without exposure.

### Attribute-Based Access Control (ABAC)
- **Complexity:** High
- **Maturity:** GA
- **Summary:** Access decisions based on user attributes (department, role, location) plus resource attributes enabling fine-grained, scalable permissions.

### Workspace Permission Governance
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** Manages workspace role assignments (Admin, Member, Contributor, Viewer) through approval workflows preventing unauthorized access creep.

### Encryption at Rest with Customer-Managed Keys
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Implements encryption at rest using customer-managed keys (CMK) stored in Azure Key Vault for OneLake workspace data. Ensures TLS 1.2+ for all data in transit and maintains FIPS 140-2 compliance for sensitive HR data.

### Data Loss Prevention Policy Enforcement
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Configures Microsoft Purview Data Loss Prevention (DLP) policies to detect and block unauthorized export or sharing of sensitive information types including SSN, salary data, and bank account numbers.

### Statistical Anonymization for HR Analytics
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Implements k-anonymity and differential privacy techniques to ensure published HR analytics cannot identify individuals through aggregation attacks or frequency analysis.

### Audit Log Export and SIEM Integration
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Forwards Fabric activity logs and Power BI audit logs to Azure Sentinel for centralized SOC monitoring, anomaly detection, and forensic investigation.

### Data Subject Request Fulfillment Pipeline
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Automates GDPR/PIPEDA data subject rights (access and erasure) with workflows using Purview data lineage, soft-delete mechanisms, and verification processes.

### Network Isolation with Private Endpoints
- **Complexity:** High
- **Maturity:** GA
- **Summary:** Implements Azure Private Endpoints for Fabric Capacity and managed private endpoints for Spark/compute, ensuring traffic flows only over private VNet and preventing internet exposure.

### Just-in-Time Privileged Access Management
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Implements Azure Entra ID Privileged Identity Management (PIM) for just-in-time elevation of workspace admin roles, with approval workflows and MFA enforcement.

### Encryption at Rest with Customer-Managed Keys
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Implements encryption at rest using customer-managed keys (CMK) stored in Azure Key Vault for OneLake workspace data. Ensures TLS 1.2+ for all data in transit and maintains FIPS 140-2 compliance for sensitive HR data.

### Data Loss Prevention Policy Enforcement
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Configures Microsoft Purview Data Loss Prevention (DLP) policies to detect and block unauthorized export or sharing of sensitive information types including SSN, salary data, and bank account numbers.

### Statistical Anonymization for HR Analytics
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Implements k-anonymity and differential privacy techniques to ensure published HR analytics cannot identify individuals through aggregation attacks or frequency analysis.

### Audit Log Export and SIEM Integration
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Forwards Fabric activity logs and Power BI audit logs to Azure Sentinel for centralized SOC monitoring, anomaly detection, and forensic investigation.

### Data Subject Request Fulfillment Pipeline
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Automates GDPR/PIPEDA data subject rights (access and erasure) with workflows using Purview data lineage, soft-delete mechanisms, and verification processes.

### Network Isolation with Private Endpoints
- **Complexity:** High
- **Maturity:** GA
- **Summary:** Implements Azure Private Endpoints for Fabric Capacity and managed private endpoints for Spark/compute, ensuring traffic flows only over private VNet and preventing internet exposure.

### Just-in-Time Privileged Access Management
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Implements Azure Entra ID Privileged Identity Management (PIM) for just-in-time elevation of workspace admin roles, with approval workflows and MFA enforcement.

---

## Business Intelligence and Reporting (Domain 4)

**Total Patterns:** 7

### Direct Lake Power BI Semantic Models
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Power BI semantic models using Direct Lake connectivity to Fabric Gold tables for real-time BI without data import.

### Storage Mode Selection (Import/DirectQuery/Dual)
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Chooses optimal storage mode per table based on size, update frequency, and performance requirements.

### Composite Models (Multi-Source Mashing)
- **Complexity:** High
- **Maturity:** GA
- **Summary:** Combines tables from multiple sources (Lakehouse, Warehouse, SQL, Excel) in single semantic model for unified analytics.

### Certified Semantic Models
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** BI team certifies semantic models ensuring consistent definitions, quality metrics, and single source of truth for organization.

### Paginated Reports for Formal Documents
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Power BI paginated reports for pixel-perfect formal documents like payroll statements, regulatory reports, and audit certifications.

### Power BI Metrics Scorecards
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** Visual display of key metrics with goals, trends, and out-of-range alerts enabling executive dashboards.

### Power BI Deployment Pipelines
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Automated promotion of BI artifacts from development through staging to production enabling controlled releases.

---

## Machine Learning and Predictive Analytics (Domain 5)

**Total Patterns:** 6

### Batch Inference Pipelines
- **Complexity:** High
- **Maturity:** GA
- **Summary:** Regular batch scoring of employee records against trained ML models producing predictions (attrition risk, salary range) at scale.

### Feature Store Implementation
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Centralized repository of engineered features (tenure_years, salary_percentile) for reuse across ML models reducing redundancy.

### MLflow Model Registry
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Centralized repository for ML models with versioning, staging (Dev/Prod), and metadata enabling model lifecycle management.

### Model Drift Detection and Monitoring
- **Complexity:** High
- **Maturity:** Preview
- **Summary:** Automated monitoring of model performance metrics detecting drift when predictions no longer match reality triggering retraining.

### Fairness and Bias Evaluation
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Evaluates ML models for bias in predictions across demographic groups (gender, race) ensuring fair and compliant hiring/promotion decisions.

### Champion-Challenger Model Testing
- **Complexity:** High
- **Maturity:** GA
- **Summary:** A/B testing of new model versions (Challenger) against current production model (Champion) in controlled experiments.

---

## Generative AI and Advanced Analytics (Domain 6)

**Total Patterns:** 7

### RAG (Retrieval-Augmented Generation) Fabric-Grounded
- **Complexity:** High
- **Maturity:** Preview
- **Summary:** LLM-powered chatbot that retrieves employee data, org structure, policies from Fabric and generates answers grounded in actual data.

### Secure Conversational Interface with RLS
- **Complexity:** High
- **Maturity:** Preview
- **Summary:** Conversational AI interface enforcing row-level security so employees see only authorized data and managers see team data.

### Azure AI Foundry Integration
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Integrates Azure AI Foundry (formerly Cognitive Services) for NLP, document understanding, and entity extraction on HR documents.

### Copilot Studio with Fabric Data Grounding
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Power Platform Copilot Studio integration with Fabric data enabling custom copilots grounded in HR analytics without custom coding.

### Semantic Search with Vector Embeddings
- **Complexity:** High
- **Maturity:** Preview
- **Summary:** Vector embeddings of HR data (job descriptions, policies, performance reviews) enabling semantic similarity search.

### LLM Auto-Generated Narratives
- **Complexity:** Medium
- **Maturity:** Preview
- **Summary:** LLM automatically generates narrative descriptions of dashboards, trends, and insights reducing reporting burden.

### HR-Specific AI Guardrails and Safety
- **Complexity:** High
- **Maturity:** Emerging
- **Summary:** Guardrails preventing AI from making inappropriate recommendations on hiring, termination, or compensation decisions.

---

## Alerting and Automation (Domain 7)

**Total Patterns:** 5

### Data Activator (Reflex) for Auto-Actions
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Automatic workflows triggered by data anomalies: high turnover in department → auto-email recruiter; forecast miss → escalate to VP.

### Power Automate Workflows with Data Triggers
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** Power Automate workflows triggered by HR data changes automating notifications, approvals, and downstream processes.

### Metric Summarization Engine
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** Automated daily/weekly email summaries of key metrics with trends and anomalies delivered to executives without manual compilation.

### SLA Freshness Monitoring
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** Monitoring pipeline SLAs ensuring data is refreshed within defined window (midnight refresh by 6am) with alerts on violations.

### Automated Escalation and Routing
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Smart routing of alerts to appropriate teams based on severity and data ownership (high turnover → dept head; data quality issue → data team).

---

## Data Sharing and Collaboration (Domain 8)

**Total Patterns:** 9

### Cross-Workspace Data Sharing via Shortcuts
- **Complexity:** Low
- **Maturity:** GA
- **Summary:** Shortcuts enable different workspaces (HR, Finance, Recruiting) to share data without copying, maintaining single source of truth.

### Cross-Tenant Data Sharing (B2B Scenarios)
- **Complexity:** High
- **Maturity:** Preview
- **Summary:** Sharing data across Azure AD tenants enabling partner organizations to access shared analytics while maintaining security.

### Semantic Model Certification Pipeline
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Automated certification workflow where data teams publish semantic models and BI team verifies quality before marking Certified.

### REST API Exposure and Management
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Expose curated analytics data via REST APIs enabling external systems (HRIS, payroll, recruiting platforms) to consume Fabric data.

### Dataset Subscription and Change Alerts
- **Complexity:** Medium
- **Maturity:** Preview
- **Summary:** Subscribers receive alerts when datasets change or refresh, enabling downstream systems to react to data updates.

### Disaster Recovery and Geo-Redundancy
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Configures OneLake with zone-redundant storage (ZRS) and geo-replication to paired Azure region, with manual failover procedures and multi-geo capacity for data residency.

### Cross-Border Data Residency Isolation
- **Complexity:** High
- **Maturity:** GA
- **Summary:** Isolates employee data by geography using multi-geo Fabric capacities, ensuring Canadian employee data remains in Canada and US data in US, with aggregate-only cross-border reporting.

### Disaster Recovery and Geo-Redundancy
- **Complexity:** Medium
- **Maturity:** GA
- **Summary:** Configures OneLake with zone-redundant storage (ZRS) and geo-replication to paired Azure region, with manual failover procedures and multi-geo capacity for data residency.

### Cross-Border Data Residency Isolation
- **Complexity:** High
- **Maturity:** GA
- **Summary:** Isolates employee data by geography using multi-geo Fabric capacities, ensuring Canadian employee data remains in Canada and US data in US, with aggregate-only cross-border reporting.

---

