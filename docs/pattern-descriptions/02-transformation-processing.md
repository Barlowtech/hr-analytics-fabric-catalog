# Transformation and Processing

Transformation and processing logic is where raw HR data becomes actionable insights. This domain encompasses
the patterns and practices for building reliable, maintainable ETL/ELT pipelines that handle everything from employee
master data to complex workforce metrics.

Effective transformation patterns ensure data consistency, enable rapid development of new analytics capabilities, and
provide visibility into how data flows through your systems. These patterns help you manage the complexity of HR data
processing while maintaining performance and reliability.

Whether you're building simple daily refreshes or complex event-driven pipelines, the patterns in this section provide
tested approaches for tackling common transformation challenges.

---

## Spark Notebook ETL Pipelines
**Complexity:** High | **Maturity:** GA
**Fabric Components:** Notebook, Spark, PySpark, Lakehouse, Delta Lake

### What It Is
Notebooks provide flexibility for complex logic, iterative development, and large-scale transformations. Payroll notebooks standardize fields, fill missing dates, calculate tenure.

### Pros
- Ultimate flexibility for complex business logic.
- Cell-level execution enables step-by-step debugging.
- Automatic scaling to large datasets.

### Cons
- Requires Python/Scala expertise.
- No visual lineage or profiling.
- Harder to govern.

### Usage Instructions
1. Create notebook. 2. Read Bronze: df = spark.read.table(). 3. Transform (standardize, validate, enrich). 4. Write to Silver. 5. Test on sample data. 6. Schedule as job. 7. Add error handling.

### Governance Considerations
> Implement code review for notebooks. Version control via Git. Restrict modify permissions. Log all transformations. Document assumptions.

### People Analytics Use Cases
- Complex payroll ETL with reconciliation.
- Employee movement tracking via snapshots.
- Unified talent dataset from multiple sources.

### Related Patterns
- **Compatible with:** medallion-architecture, delta-lake-partitioning, incremental-watermark
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

## Dataflow Gen2 Low-Code Transformations
**Complexity:** Low | **Maturity:** GA
**Fabric Components:** Dataflow Gen2, Power Query Online, Lakehouse, Power BI

### What It Is
Graphical UI for filter, merge, group, enrich. Employee master ingest, remove duplicates, rename columns, output to Lakehouse.

### Pros
- Reduces time-to-delivery for standard transforms.
- Built-in data profiling and quality checks.
- Native Power BI integration.

### Cons
- Limited to moderately complex logic.
- Performance degrades on large datasets.
- Harder to version control and CI/CD.

### Usage Instructions
1. Create Dataflow Gen2. 2. Connect to source. 3. Apply transforms: Remove Duplicates, Filter, Rename. 4. Group/summarize if needed. 5. Merge with references. 6. Preview and validate. 7. Configure destination. 8. Schedule refresh.

### Governance Considerations
> Document formulas clearly. Establish change approval. Monitor refresh times. Use as preferred entry for business users. Implement labels on outputs.

### People Analytics Use Cases
- Weekly employee snapshot: ingest, dedup, filter, output.
- Department cost center mapping and aggregation.
- Applicant data prep for recruiting analytics.

### Related Patterns
- **Compatible with:** medallion-architecture, data-quality-validation
- **Prerequisites:** None
- **Incompatible with:** None

---

## Incremental Loading with Watermarks
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Spark Notebook, Lakehouse, Delta Lake, Control Tables

### What It Is
Store max last_modified_date in control table; query only records > previous watermark. Nightly refresh hours reduces to minutes.

### Pros
- Reduces refresh from hours to minutes.
- Scales elegantly with constant change volume.
- Enables real-time/near-real-time analytics.

### Cons
- Requires reliable source change tracking.
- Complex to handle late-arriving data.
- Difficult recovery from failures.

### Usage Instructions
1. Create control table for watermarks. 2. Read previous watermark. 3. Query source with filter. 4. Merge into Silver. 5. Update watermark. 6. Monitor for late data.

### Governance Considerations
> Govern source change-tracking columns. Document watermark logic. Implement monitoring. Archive watermarks. Establish reset procedures.

### People Analytics Use Cases
- Employee transactions with daily incremental loads.
- Real-time headcount dashboard.
- Employee history capturing changes.

### Related Patterns
- **Compatible with:** medallion-architecture, spark-notebook-etl, scd-type-2
- **Prerequisites:** spark-notebook-etl, medallion-architecture
- **Incompatible with:** None

---

## Slowly Changing Dimensions Type 2
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Spark Notebook, Delta Lake, Lakehouse

### What It Is
New rows created for changes with effective_date, end_date. Promotion creates new employee row; old row marked ended. Enables salary progression analysis.

### Pros
- Enables temporal analysis and past-state reconstruction.
- Maintains historical context for metrics.
- Supports full audit trail.

### Cons
- Storage overhead from historical versions.
- Complex merge logic required.
- Analytics queries become more complex.

### Usage Instructions
1. Design dimension with surrogate key, effective_date, end_date, current_flag. 2. Initial load. 3. On update: END previous, INSERT new. 4. Merge into dimension. 5. Validate no overlaps.

### Governance Considerations
> Document merge logic thoroughly. Implement validation checks. Archive old dimensions. Use selectively. Establish retention policies.

### People Analytics Use Cases
- Career progression analysis with salary growth.
- Org change analysis with historical reporting lines.
- Compensation cohort analysis.

### Related Patterns
- **Compatible with:** medallion-architecture, spark-notebook-etl, incremental-watermark
- **Prerequisites:** spark-notebook-etl, medallion-architecture
- **Incompatible with:** None

---

## Change Data Capture (CDC) for Auditing
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Warehouse, Spark Notebook, Audit Tables

### What It Is
Salary update triggers record logging old/new values. Audit table captures INSERT/UPDATE/DELETE with metadata. Supports investigations.

### Pros
- Complete audit trail for compliance.
- Enables real-time alerting on sensitive changes.
- Supports efficient incremental processing.

### Cons
- Increases write overhead and latency.
- Audit tables grow very large.
- Edge cases require careful handling.

### Usage Instructions
1. Create audit table. 2. Trigger on updates records changes. 3. Archive records >7 years. 4. Expose to compliance via Power BI. 5. Set up alerts.

### Governance Considerations
> Restrict to compliance/audit only. Establish retention policies. Document audited fields. Archive to cold storage. Use for investigation support.

### People Analytics Use Cases
- Compliance auditing of salary changes.
- Detecting unauthorized modifications.
- Payroll reconciliation tracking.

### Related Patterns
- **Compatible with:** sensitivity-labels, scd-type-2, data-quality-validation
- **Prerequisites:** None
- **Incompatible with:** None

---

## dbt Integration for Data Transformation
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Warehouse, Lakehouse, dbt, Git, Spark SQL

### What It Is
dbt projects organize SQL transformations with tests, lineage, documentation. Junior analysts contribute familiar SQL; dbt handles plumbing.

### Pros
- Brings software engineering to analytics.
- Modular SQL enables junior analyst contribution.
- Auto-generates lineage documentation.

### Cons
- Requires dbt and YAML knowledge.
- Performance tuning less transparent.
- Limited to SQL transformations.

### Usage Instructions
1. Create dbt project. 2. Configure Warehouse target. 3. Write SQL models. 4. Define tests. 5. Run dbt run. 6. Commit to git. 7. Configure CI/CD.

### Governance Considerations
> Structure by medallion layers. Implement code review. Use dbt tests for quality. Document business context. Manage breaking changes carefully.

### People Analytics Use Cases
- HR transformation logic with employee, role, compensation models.
- Collaborative analysis pipeline with code review.
- Rapid metrics iteration.

### Related Patterns
- **Compatible with:** medallion-architecture, data-quality-validation, spark-notebook-etl
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

## Data Quality Validation Framework
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Spark Notebook, dbt, Great Expectations, Lakehouse

### What It Is
Validation tests NULL values in required fields, validates salary ranges, confirms dept codes match reference, detects duplicates. Failures pause processes.

### Pros
- Catches issues at source before propagation.
- Builds analyst trust in data.
- Enables quick root-cause analysis.

### Cons
- Requires upfront effort to define rules.
- Can over-reject valid data.
- Adds latency to pipelines.

### Usage Instructions
1. Define rules: required_fields, ranges, valid values. 2. After load, run validation. 3. Check violations vs threshold. 4. Alert if exceeded. 5. Implement with dbt tests or Great Expectations.

### Governance Considerations
> Document rules with justification. Version in code. Archive results for audits. Use as data contract documentation. Establish escalation procedures.

### People Analytics Use Cases
- Payroll validation before Finance handoff.
- Org hierarchy consistency checking.
- HRIS reconciliation.

### Related Patterns
- **Compatible with:** medallion-architecture, spark-notebook-etl, dbt-integration
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

## PII Tokenization and Pseudonymization
**Complexity:** High | **Maturity:** Emerging
**Fabric Components:** Fabric Notebooks, PySpark, Microsoft Presidio, Azure Key Vault, Lakehouse

### What It Is
PII tokenization uses deterministic hashing to replace sensitive personal identifiers with tokens while maintaining the ability to link records. Microsoft Presidio, an AI-powered data protection service, automatically detects PII entities (names, addresses, phone numbers, emails) within notebooks and datasets. Identified PII is replaced with tokens, with the mapping stored securely in Azure Key Vault. For HR analytics, this enables sharing anonymized talent data with third-party vendors, consultants, and development teams without exposing actual employee identity. Deterministic tokenization (same PII always maps to same token) preserves join semantics. PySpark transformations within Fabric Notebooks perform tokenization at scale. Different token formats support different use cases: hash tokens for aggregate analytics, UUID tokens for record-level joins. Reverse lookup tokens require Key Vault authorization for decryption.

### Pros
- Enables secure data sharing with business partners and vendors by removing actual identity without losing join capability.
- Detects PII automatically using AI models rather than relying on manual regex patterns, catching complex PII patterns.
- Supports different tokenization strategies per use case: hash-only tokens for analytics, reversible tokens for authorized users with Key Vault access.

### Cons
- Deterministic tokenization vulnerable to frequency analysis if PII distribution is skewed (e.g., only 3 VP names).
- Presidio requires pre-trained models and tuning to avoid false positives/negatives in organization-specific contexts.
- Large-scale tokenization can impact notebook execution time; requires parallel PySpark processing for efficiency.

### Usage Instructions
1. Install Presidio in Fabric Notebook: pip install presidio-analyzer presidio-anonymizer. 2. Load employee data in PySpark DataFrame. 3. Configure Presidio analyzer with entity patterns: PERSON, PHONE_NUMBER, EMAIL_ADDRESS. 4. Create tokenization mapping: use Presidio to detect PII, generate deterministic SHA-256 hash token or UUID. 5. Store mapping in Key Vault secret with access restricted to governance team. 6. Replace PII with tokens using Presidio anonymizer. 7. Save tokenized dataset to Silver/Gold layer. 8. Log all tokenization operations with user, timestamp, entity count. 9. Test reverse lookup process with authorized user.

### Governance Considerations
> Establish PII tokenization review board with privacy, security, and HR stakeholders. Document which entity types are tokenized and which remain for legitimate analytics. Implement access controls requiring Key Vault authorization for reverse lookups. Monitor tokenization logs for suspicious decryption patterns. Conduct quarterly audits of Presidio configuration to ensure no drift in entity detection. Maintain separate tokenization keys per data consumer or use case.

### People Analytics Use Cases
- Sharing anonymized employee experience survey data with external consulting firm to analyze cultural trends without exposing employee names, emails, or departments.
- Enabling development team to use production-like employee hierarchy and org structure data for testing without accessing real employee identities, using UUID tokens in place of names.
- Providing recruitment analytics to third-party recruitment platform showing skills and experience patterns without revealing actual employee identity, enabling vendor to match internal talent to opportunities.

### Related Patterns
- **Compatible with:** medallion-architecture, spark-notebook-etl, data-quality-validation, dlp-policy-enforcement
- **Prerequisites:** None
- **Incompatible with:** None

---

## Automated Data Retention and Purge Pipeline
**Complexity:** High | **Maturity:** Emerging
**Fabric Components:** Data Factory Pipeline, Fabric Notebooks, OneLake, Delta Lake, Lakehouse

### What It Is
Data retention and purge pipelines ensure that employee data is not retained longer than required by law or business policy. For HR analytics, employee records must be retained per employment law (typically 3-7 years depending on jurisdiction), then securely deleted. Automated pipelines check record creation/modification dates against configurable retention policies, identify data eligible for purge, execute secure deletion via soft-delete flags or physical removal, and generate audit logs. Legal holds prevent deletion during litigation or regulatory investigations. Data Factory pipelines coordinate with Fabric notebooks to identify eligible records using SQL queries (SELECT * WHERE modified_date < DATEADD(year,-3,GETDATE())), mark for deletion, execute deletion operations, and log to audit tables. Soft-delete approach (marking records inactive) preserves referential integrity and enables recovery. Hard-delete (physical removal from Delta Lake) reduces storage and improves query performance but requires careful execution.

### Pros
- Automates compliance with data retention regulations (GDPR right-to-erasure, employment law, SOX records retention).
- Reduces storage costs by removing obsolete data and improves query performance on smaller active datasets.
- Maintains complete audit trail of deleted records and reasons, supporting forensic investigations and compliance audits.

### Cons
- Incorrectly configured retention rules can cause accidental data loss; requires thorough testing and change management approval.
- Soft-delete approaches maintain referential integrity but require query filters to exclude deleted records; hard-delete is faster but riskier.
- Legal holds must be tracked separately; coordination between legal, HR, and data teams is required to manage hold status.

### Usage Instructions
1. Define retention policies in configuration table: entity type, retention period (years), jurisdiction, legal hold indicator. 2. Create Data Factory pipeline with Copy Activity to identify records eligible for purge using SQL: SELECT * WHERE datediff(year, modified_date, getdate()) >= retention_years AND legal_hold = 0. 3. Use Fabric Notebook to mark records as deleted (UPDATE table SET is_deleted = 1 WHERE id IN (...)) instead of hard delete initially. 4. Execute soft-delete daily/weekly per schedule. 5. After 30-day recovery period, run hard delete: VACUUM table_name RETAIN 0 HOURS; DELETE FROM table WHERE is_deleted = 1. 6. Log all operations: user, timestamp, record count, reasons. 7. Send audit report to compliance/legal team monthly.

### Governance Considerations
> Establish data retention committee with legal, HR, compliance, and data teams. Document retention policies for each data entity type by jurisdiction. Implement approval workflow for legal hold changes. Set up audit alerts for large purge operations. Conduct quarterly audits of purge logs to verify correctness. Test disaster recovery to ensure deleted data cannot be recovered from backups without explicit authorization. Maintain retention policy version control.

### People Analytics Use Cases
- Automatically delete contingent worker records 2 years after separation date and contract end, enabling compliance with employment laws while reducing data footprint.
- Purge applicant data after hiring decision per FCRA requirements (typically 3 years), except for records under litigation hold from employment disputes.
- Soft-delete employee benefit elections from terminated employees after 7 years but preserve audit trail for pension calculations and benefit inquiries, with legal hold preventing deletion during claims.

### Related Patterns
- **Compatible with:** medallion-architecture, spark-notebook-etl, delta-lake-partitioning, audit-siem-integration
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

## Dual-Approval Change Management Pipeline
**Complexity:** Medium | **Maturity:** Emerging
**Fabric Components:** Azure DevOps, Data Factory Pipeline, Fabric Deployment Pipelines, Git Integration

### What It Is
Four-eyes principle requires two independent approvals before changes to production systems. For HR analytics, changes to data pipelines (transformations, data quality rules, refresh schedules) can affect payroll, benefits, or compliance analytics. Requiring dual approval ensures both business correctness (HR manager) and governance compliance (data governance officer) are verified. Azure DevOps Deployment Pipelines implement gates between environments: development -> staging -> production. Staging gate requires business approval from HR analytics owner confirming transformations are correct. Production gate requires data governance approval confirming RLS policies, data lineage, and compliance are maintained. Pull request reviews enforce code quality and documentation before merge to main. Git branching strategy separates features, requiring peer review. Change log automatically documents approvers, timestamp, and change summary. Rejection of changes includes audit trail for compliance.

### Pros
- Enforces dual approval, preventing single-person errors and unauthorized changes to critical analytics.
- Creates audit trail proving compliance with change control requirements, supporting SOX, HIPAA audits.
- Improves quality by requiring peer review before production deployment.

### Cons
- Adds cycle time: waiting for two approvers can delay urgent fixes (typical cycle time 24-48 hours).
- Requires both approvers to be available; absence of approver blocks deployment.
- False sense of security if approvers don't actually review changes carefully.

### Usage Instructions
1. Set up Azure DevOps project with Git repo for Fabric pipeline definitions. 2. Configure branch policy on main: require pull request reviews, minimum 2 approvers (business + governance), status checks passing. 3. Create staging deployment pipeline: trigger on PR approval, deploy to staging environment. 4. Add pre-deployment gate before staging: auto-approve (runs tests, validates syntax). 5. Add pre-deployment gate before production: manual approval, allow only specific users (data governance team). Require justification/description. 6. Create business approval gate: HR manager reviews transformations, confirms correctness. 7. Track approvals: Azure DevOps automatically logs timestamp, approver identity, comments. 8. Reject approvals include mandatory reason. 9. Create dashboard: count deployments, approval time metrics, rejection rates. 10. Quarterly review: analyze approval bottlenecks, optimize process.

### Governance Considerations
> Define who can request, approve, and reject changes: business sponsor (business approval), data governance (compliance approval). Document approval criteria: business approval verifies transformations match requirements, governance approval verifies RLS, lineage, data quality, compliance. Implement escalation path for urgent changes (e.g., 24-hour SLA for critical bug fixes). Audit approval logs monthly. Require documented change rationale in pull request. Disallow approval from same person who submitted change (dual-approval enforced technically).

### People Analytics Use Cases
- Data engineer submits PR changing employee salary aggregation logic (e.g., fixing bonus calculation). Business sponsor (payroll manager) approves confirming calculation is correct. Data governance approves confirming aggregation preserves privacy (k>=5). Production deployment occurs only after both approvals.
- New HR dataset onboarded to Lakehouse: ingestion pipeline PR submitted. Business sponsor approves confirming data matches HRIS system. Data governance approves confirming sensitivity labels assigned, lineage documented. Both approvals required before prod activation.
- Urgent hotfix: salary dashboard showing incorrect totals. Change submitted with 'urgent' flag. Both approvers pinged, typically respond within 2-4 hours. Production deployment after both approvals.

### Related Patterns
- **Compatible with:** deployment-pipelines, audit-siem-integration
- **Prerequisites:** None
- **Incompatible with:** None

---

## PII Tokenization and Pseudonymization
**Complexity:** High | **Maturity:** Emerging
**Fabric Components:** Fabric Notebooks, PySpark, Microsoft Presidio, Azure Key Vault, Lakehouse

### What It Is
PII tokenization uses deterministic hashing to replace sensitive personal identifiers with tokens while maintaining the ability to link records. Microsoft Presidio, an AI-powered data protection service, automatically detects PII entities (names, addresses, phone numbers, emails) within notebooks and datasets. Identified PII is replaced with tokens, with the mapping stored securely in Azure Key Vault. For HR analytics, this enables sharing anonymized talent data with third-party vendors, consultants, and development teams without exposing actual employee identity. Deterministic tokenization (same PII always maps to same token) preserves join semantics. PySpark transformations within Fabric Notebooks perform tokenization at scale. Different token formats support different use cases: hash tokens for aggregate analytics, UUID tokens for record-level joins. Reverse lookup tokens require Key Vault authorization for decryption.

### Pros
- Enables secure data sharing with business partners and vendors by removing actual identity without losing join capability.
- Detects PII automatically using AI models rather than relying on manual regex patterns, catching complex PII patterns.
- Supports different tokenization strategies per use case: hash-only tokens for analytics, reversible tokens for authorized users with Key Vault access.

### Cons
- Deterministic tokenization vulnerable to frequency analysis if PII distribution is skewed (e.g., only 3 VP names).
- Presidio requires pre-trained models and tuning to avoid false positives/negatives in organization-specific contexts.
- Large-scale tokenization can impact notebook execution time; requires parallel PySpark processing for efficiency.

### Usage Instructions
1. Install Presidio in Fabric Notebook: pip install presidio-analyzer presidio-anonymizer. 2. Load employee data in PySpark DataFrame. 3. Configure Presidio analyzer with entity patterns: PERSON, PHONE_NUMBER, EMAIL_ADDRESS. 4. Create tokenization mapping: use Presidio to detect PII, generate deterministic SHA-256 hash token or UUID. 5. Store mapping in Key Vault secret with access restricted to governance team. 6. Replace PII with tokens using Presidio anonymizer. 7. Save tokenized dataset to Silver/Gold layer. 8. Log all tokenization operations with user, timestamp, entity count. 9. Test reverse lookup process with authorized user.

### Governance Considerations
> Establish PII tokenization review board with privacy, security, and HR stakeholders. Document which entity types are tokenized and which remain for legitimate analytics. Implement access controls requiring Key Vault authorization for reverse lookups. Monitor tokenization logs for suspicious decryption patterns. Conduct quarterly audits of Presidio configuration to ensure no drift in entity detection. Maintain separate tokenization keys per data consumer or use case.

### People Analytics Use Cases
- Sharing anonymized employee experience survey data with external consulting firm to analyze cultural trends without exposing employee names, emails, or departments.
- Enabling development team to use production-like employee hierarchy and org structure data for testing without accessing real employee identities, using UUID tokens in place of names.
- Providing recruitment analytics to third-party recruitment platform showing skills and experience patterns without revealing actual employee identity, enabling vendor to match internal talent to opportunities.

### Related Patterns
- **Compatible with:** medallion-architecture, spark-notebook-etl, data-quality-validation, dlp-policy-enforcement
- **Prerequisites:** None
- **Incompatible with:** None

---

## Automated Data Retention and Purge Pipeline
**Complexity:** High | **Maturity:** Emerging
**Fabric Components:** Data Factory Pipeline, Fabric Notebooks, OneLake, Delta Lake, Lakehouse

### What It Is
Data retention and purge pipelines ensure that employee data is not retained longer than required by law or business policy. For HR analytics, employee records must be retained per employment law (typically 3-7 years depending on jurisdiction), then securely deleted. Automated pipelines check record creation/modification dates against configurable retention policies, identify data eligible for purge, execute secure deletion via soft-delete flags or physical removal, and generate audit logs. Legal holds prevent deletion during litigation or regulatory investigations. Data Factory pipelines coordinate with Fabric notebooks to identify eligible records using SQL queries (SELECT * WHERE modified_date < DATEADD(year,-3,GETDATE())), mark for deletion, execute deletion operations, and log to audit tables. Soft-delete approach (marking records inactive) preserves referential integrity and enables recovery. Hard-delete (physical removal from Delta Lake) reduces storage and improves query performance but requires careful execution.

### Pros
- Automates compliance with data retention regulations (GDPR right-to-erasure, employment law, SOX records retention).
- Reduces storage costs by removing obsolete data and improves query performance on smaller active datasets.
- Maintains complete audit trail of deleted records and reasons, supporting forensic investigations and compliance audits.

### Cons
- Incorrectly configured retention rules can cause accidental data loss; requires thorough testing and change management approval.
- Soft-delete approaches maintain referential integrity but require query filters to exclude deleted records; hard-delete is faster but riskier.
- Legal holds must be tracked separately; coordination between legal, HR, and data teams is required to manage hold status.

### Usage Instructions
1. Define retention policies in configuration table: entity type, retention period (years), jurisdiction, legal hold indicator. 2. Create Data Factory pipeline with Copy Activity to identify records eligible for purge using SQL: SELECT * WHERE datediff(year, modified_date, getdate()) >= retention_years AND legal_hold = 0. 3. Use Fabric Notebook to mark records as deleted (UPDATE table SET is_deleted = 1 WHERE id IN (...)) instead of hard delete initially. 4. Execute soft-delete daily/weekly per schedule. 5. After 30-day recovery period, run hard delete: VACUUM table_name RETAIN 0 HOURS; DELETE FROM table WHERE is_deleted = 1. 6. Log all operations: user, timestamp, record count, reasons. 7. Send audit report to compliance/legal team monthly.

### Governance Considerations
> Establish data retention committee with legal, HR, compliance, and data teams. Document retention policies for each data entity type by jurisdiction. Implement approval workflow for legal hold changes. Set up audit alerts for large purge operations. Conduct quarterly audits of purge logs to verify correctness. Test disaster recovery to ensure deleted data cannot be recovered from backups without explicit authorization. Maintain retention policy version control.

### People Analytics Use Cases
- Automatically delete contingent worker records 2 years after separation date and contract end, enabling compliance with employment laws while reducing data footprint.
- Purge applicant data after hiring decision per FCRA requirements (typically 3 years), except for records under litigation hold from employment disputes.
- Soft-delete employee benefit elections from terminated employees after 7 years but preserve audit trail for pension calculations and benefit inquiries, with legal hold preventing deletion during claims.

### Related Patterns
- **Compatible with:** medallion-architecture, spark-notebook-etl, delta-lake-partitioning, audit-siem-integration
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

## Dual-Approval Change Management Pipeline
**Complexity:** Medium | **Maturity:** Emerging
**Fabric Components:** Azure DevOps, Data Factory Pipeline, Fabric Deployment Pipelines, Git Integration

### What It Is
Four-eyes principle requires two independent approvals before changes to production systems. For HR analytics, changes to data pipelines (transformations, data quality rules, refresh schedules) can affect payroll, benefits, or compliance analytics. Requiring dual approval ensures both business correctness (HR manager) and governance compliance (data governance officer) are verified. Azure DevOps Deployment Pipelines implement gates between environments: development -> staging -> production. Staging gate requires business approval from HR analytics owner confirming transformations are correct. Production gate requires data governance approval confirming RLS policies, data lineage, and compliance are maintained. Pull request reviews enforce code quality and documentation before merge to main. Git branching strategy separates features, requiring peer review. Change log automatically documents approvers, timestamp, and change summary. Rejection of changes includes audit trail for compliance.

### Pros
- Enforces dual approval, preventing single-person errors and unauthorized changes to critical analytics.
- Creates audit trail proving compliance with change control requirements, supporting SOX, HIPAA audits.
- Improves quality by requiring peer review before production deployment.

### Cons
- Adds cycle time: waiting for two approvers can delay urgent fixes (typical cycle time 24-48 hours).
- Requires both approvers to be available; absence of approver blocks deployment.
- False sense of security if approvers don't actually review changes carefully.

### Usage Instructions
1. Set up Azure DevOps project with Git repo for Fabric pipeline definitions. 2. Configure branch policy on main: require pull request reviews, minimum 2 approvers (business + governance), status checks passing. 3. Create staging deployment pipeline: trigger on PR approval, deploy to staging environment. 4. Add pre-deployment gate before staging: auto-approve (runs tests, validates syntax). 5. Add pre-deployment gate before production: manual approval, allow only specific users (data governance team). Require justification/description. 6. Create business approval gate: HR manager reviews transformations, confirms correctness. 7. Track approvals: Azure DevOps automatically logs timestamp, approver identity, comments. 8. Reject approvals include mandatory reason. 9. Create dashboard: count deployments, approval time metrics, rejection rates. 10. Quarterly review: analyze approval bottlenecks, optimize process.

### Governance Considerations
> Define who can request, approve, and reject changes: business sponsor (business approval), data governance (compliance approval). Document approval criteria: business approval verifies transformations match requirements, governance approval verifies RLS, lineage, data quality, compliance. Implement escalation path for urgent changes (e.g., 24-hour SLA for critical bug fixes). Audit approval logs monthly. Require documented change rationale in pull request. Disallow approval from same person who submitted change (dual-approval enforced technically).

### People Analytics Use Cases
- Data engineer submits PR changing employee salary aggregation logic (e.g., fixing bonus calculation). Business sponsor (payroll manager) approves confirming calculation is correct. Data governance approves confirming aggregation preserves privacy (k>=5). Production deployment occurs only after both approvals.
- New HR dataset onboarded to Lakehouse: ingestion pipeline PR submitted. Business sponsor approves confirming data matches HRIS system. Data governance approves confirming sensitivity labels assigned, lineage documented. Both approvals required before prod activation.
- Urgent hotfix: salary dashboard showing incorrect totals. Change submitted with 'urgent' flag. Both approvers pinged, typically respond within 2-4 hours. Production deployment after both approvals.

### Related Patterns
- **Compatible with:** deployment-pipelines, audit-siem-integration
- **Prerequisites:** None
- **Incompatible with:** None

---

