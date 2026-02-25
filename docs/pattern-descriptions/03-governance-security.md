# Governance and Security

HR data is among the most sensitive information in any organization. Employee records, compensation details,
and performance information require careful governance, strong security controls, and audit trails that satisfy both
regulatory requirements and organizational policies.

This domain focuses on patterns for implementing role-based access control, data lineage tracking, compliance monitoring,
and secure data sharing. These patterns help you build trust in your analytics platform while meeting governance obligations.

Strong governance enables faster, more confident decision-making by ensuring that everyone accessing HR analytics has
appropriate access, understands the data lineage, and operates within defined policies.

---

## Microsoft Purview Data Map
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Microsoft Purview, Fabric, Lakehouse, Warehouse

### What It Is
Purview scans Fabric workspace discovering tables, columns, lineage. Classifications mark PII (SSN, salary). Stewards govern assets and ownership.

### Pros
- Provides complete asset inventory and lineage.
- Automates sensitive data discovery.
- Enables steward governance at scale.

### Cons
- Requires significant setup and configuration.
- Scans can be resource-intensive.
- Learning curve for Purview concepts.

### Usage Instructions
1. Connect Fabric to Purview. 2. Configure scans. 3. Run scans. 4. Review classifications. 5. Assign stewards. 6. Create business glossary. 7. Document assets.

### Governance Considerations
> Use Purview as source of truth for data governance. Integrate classifications with sensitivity labels. Assign stewards for critical assets. Track data quality metrics. Update regularly.

### People Analytics Use Cases
- Discover all HR data assets across organization.
- Track payroll data lineage from source to reports.
- Identify PII exposure and mitigation paths.

### Related Patterns
- **Compatible with:** sensitivity-labels, row-level-security, cdc-change-capture
- **Prerequisites:** None
- **Incompatible with:** None

---

## Sensitivity Labels for Data Classification
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Sensitivity Labels, Purview, Lakehouse, Warehouse, Power BI

### What It Is
Label SSN and salary columns as Highly Confidential; Purview enforces masking and restricts query results. Labels cascade to reports and exports.

### Pros
- Automated protection based on content classification.
- Enforcement applies across Fabric and Power BI.
- Cascades to exports and reports.

### Cons
- Initial labeling requires effort.
- Label enforcement can break some use cases.
- Requires governance process.

### Usage Instructions
1. Define label taxonomy. 2. Create labels in Security & Compliance. 3. Apply to tables/columns. 4. Configure label policies. 5. Test masking. 6. Monitor usage.

### Governance Considerations
> Establish consistent label taxonomy. Assign classification responsibility. Monitor label compliance. Update as data changes. Train users.

### People Analytics Use Cases
- Mark SSN, salary, health data as Highly Confidential.
- Restrict export of labeled data.
- Auto-mask salary in development environment.

### Related Patterns
- **Compatible with:** purview-data-map, row-level-security, dynamic-data-masking
- **Prerequisites:** None
- **Incompatible with:** None

---

## Row-Level Security (RLS) at Gold Layer
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Warehouse, Semantic Model, Power BI, RLS Roles

### What It Is
RLS rules evaluated at query time. HR admin sees all employees; manager sees only direct reports. Prevents accidental overexposure.

### Pros
- Query-time enforcement is performant.
- Prevents overexposure through accidental queries.
- Works across Warehouse and Power BI.

### Cons
- RLS logic can become complex.
- Debugging RLS issues is difficult.
- Semantic model must support RLS columns.

### Usage Instructions
1. Identify RLS dimension (e.g., manager_id, department). 2. Create Warehouse views with RLS. 3. In semantic model, define RLS roles. 4. Map users to roles. 5. Test query results per role. 6. Assign roles to users.

### Governance Considerations
> RLS is critical for HR data. Test thoroughly before production. Document RLS logic. Monitor for overexposure. Update when org changes.

### People Analytics Use Cases
- Managers see direct reports salary; executives see all.
- Employees see personal data only.
- HR sees department; Finance sees cost center salary.

### Related Patterns
- **Compatible with:** medallion-architecture, sensitivity-labels, certified-semantic-model
- **Prerequisites:** None
- **Incompatible with:** None

---

## Dynamic Data Masking for Development/Test
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Warehouse, Spark Notebook, Data Masking Policies

### What It Is
Replace salary values with 0, truncate SSN to last 4 digits, replace names with 'Employee-123'. Development team tests with masked data.

### Pros
- Enables realistic testing without sensitive data exposure.
- Reduces security incidents from dev environment breaches.
- Supports faster dev cycles without data sanitization.

### Cons
- Masking logic can affect performance.
- Developers frustrated by realistic data lack.
- Complex to mask consistently.

### Usage Instructions
1. Create dev/test environments. 2. Define masking rules for sensitive columns. 3. Apply masks on data refresh. 4. Validate masking prevents identification. 5. Monitor compliance.

### Governance Considerations
> Mask all sensitive data in non-prod. Maintain consistent masking across all clones. Document masking rules. Monitor mask effectiveness.

### People Analytics Use Cases
- Dev database with masked SSN, salary for developers.
- Test environment with realistic structure but masked values.
- Compliance environment with redacted data.

### Related Patterns
- **Compatible with:** sensitivity-labels, row-level-security
- **Prerequisites:** None
- **Incompatible with:** None

---

## Attribute-Based Access Control (ABAC)
**Complexity:** High | **Maturity:** GA
**Fabric Components:** Workspace Permissions, Semantic Model Roles, Azure AD Groups

### What It Is
Role/department attributes determine access. HR team member + HR resource = access. Scales better than managing individual user permissions.

### Pros
- Scales to large organizations.
- Changes managed through attributes, not user lists.
- Reduces permission management overhead.

### Cons
- Requires attribute governance.
- Complex logic can be hard to audit.
- Debugging attribute-based denials difficult.

### Usage Instructions
1. Define access attributes. 2. Populate attributes in Azure AD. 3. Create Azure AD groups by attributes. 4. Assign groups to Workspace/Model roles. 5. Test access per attribute combination. 6. Monitor attribute changes.

### Governance Considerations
> Attribute definitions require business input. Master attributes in Azure AD. Audit attribute changes. Regular access reviews. Update as org changes.

### People Analytics Use Cases
- Department attribute controls workspace access.
- Role attribute determines semantic model permissions.
- Location attribute gates data access.
- Manager attribute enables RLS.

### Related Patterns
- **Compatible with:** row-level-security, workspace-permission-governance
- **Prerequisites:** None
- **Incompatible with:** None

---

## Workspace Permission Governance
**Complexity:** Low | **Maturity:** GA
**Fabric Components:** Workspaces, Roles, Azure AD, Access Reviews

### What It Is
Access requests go through approval. Quarterly access reviews. Admins audit who has what role. Revoke unused access promptly.

### Pros
- Prevents unauthorized access accumulation.
- Audit trail of who approves access.
- Regular reviews catch stale access.

### Cons
- Adds overhead to access provisioning.
- Review fatigue with many users.
- Requires disciplined process.

### Usage Instructions
1. Define role matrix. 2. Establish request process. 3. Configure approval workflow. 4. Quarterly access review. 5. Deprovision unused access. 6. Audit log.

### Governance Considerations
> Clear role definitions. Documented request process. Approval authority defined. Review frequency set. Audit logged.

### People Analytics Use Cases
- Request approval for workspace access.
- Quarterly review of HR Analytics workspace roles.
- Audit trail for compliance.

### Related Patterns
- **Compatible with:** abac-access-control, purview-data-map
- **Prerequisites:** None
- **Incompatible with:** None

---

## Encryption at Rest with Customer-Managed Keys
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Azure Key Vault, OneLake, Fabric Workspace Settings, Entra ID Service Principal

### What It Is
Customer-Managed Key (CMK) encryption provides organizational control over encryption key lifecycle and rotation. In financial services HR analytics, CMK encryption via Azure Key Vault ensures that OneLake workspace data is encrypted with keys managed by your organization, not Microsoft. All data in transit uses TLS 1.2 or higher. This approach meets regulatory requirements for key custody, enables key rotation policies, supports audit logging for key access, and provides compliance with FIPS 140-2 standards for handling highly sensitive employee financial and personal data. Integration with Entra ID service principals allows role-based access control over decryption operations.

### Pros
- Provides organizational control over encryption keys with full audit trail of key access and rotations.
- Enables compliance with regulations requiring customer-managed encryption (SOX, GDPR, PIPEDA, HIPAA).
- Supports break-glass emergency key access protocols and disaster recovery scenarios.

### Cons
- Increases operational complexity requiring key rotation and lifecycle management procedures.
- Key Vault service calls add latency to Fabric operations, typically <10ms but noticeable at scale.
- Requires careful IAM design to prevent accidental key lockout that could make data unrecoverable.

### Usage Instructions
1. Create an Azure Key Vault resource in the same region as Fabric capacity. 2. Generate RSA 3072-bit or 4096-bit CMK in Key Vault. 3. Grant Fabric capacity system-assigned managed identity Key Wrap/Unwrap permissions on the key. 4. In Fabric Workspace Settings, select 'Customer Managed Key' and specify the Key Vault URI. 5. Configure key rotation policy (annual minimum). 6. Enable Key Vault audit logging and monitor access. 7. Test disaster recovery failover procedures quarterly.

### Governance Considerations
> Establish a key management committee with business and security stakeholders. Document key rotation procedures and emergency access protocols. Implement access reviews quarterly for Key Vault permissions. Ensure backup keys are stored in a geographically separate region. Monitor failed decryption attempts and investigate anomalies. Integrate key rotation events into change management processes.

### People Analytics Use Cases
- Salary survey analysis where payroll data is encrypted with organization-controlled CMK, enabling internal audits while maintaining key custody.
- Executive compensation dashboards requiring SOX compliance where CMK encryption demonstrates regulatory control over sensitive executive personal data.
- International employee equity tracking where Canadian employee data uses Canadian Key Vault instance and US data uses US Key Vault for data residency compliance.

### Related Patterns
- **Compatible with:** sensitivity-labels, purview-data-map, dynamic-data-masking, row-level-security
- **Prerequisites:** None
- **Incompatible with:** None

---

## Data Loss Prevention Policy Enforcement
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Microsoft Purview DLP, Sensitivity Labels, Power BI, OneLake

### What It Is
Data Loss Prevention (DLP) policies in Microsoft Purview automatically detect sensitive information types within Fabric and Power BI, then enforce preventive or detective controls. For HR analytics, DLP policies identify patterns matching US Social Security Numbers, salary ranges, employee IDs, and bank account numbers. When detected, policies can block exports to CSV/Excel, prevent uploads to personal OneDrive, restrict sharing to external domains, require approval for sensitive queries, or log incidents to Azure Sentinel for SOC review. DLP works alongside sensitivity labels to provide multi-layered protection. Policies can be scoped to specific workspaces, datasets, or semantic models. Integration with Sensitivity Labels and Power BI Workspace settings ensures consistent enforcement across analytics surfaces.

### Pros
- Detects sensitive data automatically using built-in and custom regex patterns without manual classification.
- Blocks unauthorized export at the point of action (export, copy, print) reducing insider threat risk.
- Provides audit trail of blocked/allowed actions and integrates with SIEM for incident response workflows.

### Cons
- Can trigger false positives on benign data patterns, requiring regular tuning and user exceptions.
- DLP policies are primarily detective in Power BI; preventive enforcement requires specific workspace integration.
- Regex patterns for custom sensitive data types require security team expertise and ongoing maintenance.

### Usage Instructions
1. Open Microsoft Purview Compliance Center and navigate to Data Loss Prevention > Policies. 2. Create new policy with template 'Financial Info' or 'PII' as baseline. 3. Add custom sensitive info types: SSN regex (^\d{3}-\d{2}-\d{4}$), salary range (\$[0-9]{3,4}[KM]). 4. Configure rule actions: 'Restrict access' for Power BI, 'Require justification' for exports, 'Send alert to admin'. 5. Set policy scope to HR workspace and datasets. 6. Enable incident reporting to Azure Sentinel. 7. Test policy with sample data before production rollout. 8. Review blocked incidents monthly.

### Governance Considerations
> Establish a DLP governance committee with HR, security, and legal teams. Document all custom sensitive data type patterns and business justification. Implement exception request workflow with business and compliance approval. Monitor false positive rate and adjust thresholds quarterly. Ensure DLP incidents are correlated with user access logs and audit trails. Train HR analytics team on compliant export procedures.

### People Analytics Use Cases
- Automated blocking of salary equity analysis exports containing aggregated ranges to unauthorized recipients, while allowing HR team to export to approved HR department network shares.
- Detection and alert when employee benefit election data containing SSN is copied to clipboard or exported to personal email, triggering incident response investigation.
- Prevention of executive compensation dashboard drill-through exports to external consultants without pre-approval workflow, enforcing approval for sensitive roles.

### Related Patterns
- **Compatible with:** sensitivity-labels, row-level-security, dynamic-data-masking, audit-siem-integration
- **Prerequisites:** sensitivity-labels
- **Incompatible with:** None

---

## Statistical Anonymization for HR Analytics
**Complexity:** High | **Maturity:** Emerging
**Fabric Components:** Fabric Warehouse, SQL Analytics Endpoint, PySpark Notebooks, Lakehouse

### What It Is
K-anonymity ensures that any combination of quasi-identifiers (age, department, salary band) appears in at least k records, preventing record linkage attacks. Differential privacy adds carefully calibrated noise to query results, enabling accurate aggregate statistics while preventing inference of individual values. For HR analytics, aggregation-only views enforce k-anonymity by requiring HAVING COUNT(*) >= 5 clauses on all queries, preventing disclosure of rare populations (e.g., the sole executive in a location). Noise injection adds Laplace or Gaussian noise proportional to sensitivity, with epsilon (privacy budget) controlling noise magnitude. Views in Fabric Warehouse or SQL Analytics Endpoint implement these controls. PySpark notebooks implement noise injection for ad-hoc analyses. Practical applications include publishing salary bands by role (not individuals), showing headcount by department (minimum 5 per group), and publishing engagement scores by location-function groups.

### Pros
- Provides formal mathematical guarantees against re-identification attacks, meeting GDPR and other privacy regulations' proportionality requirements.
- Enables publishing aggregate HR analytics to broad audiences (all employees, board, public) without risk of individual inference.
- Can be implemented as database views and functions, integrating seamlessly into existing analytics without changing consuming applications.

### Cons
- K-anonymity vulnerable to semantic attacks if quasi-identifiers are not carefully chosen; requires domain expertise to identify all identifying combinations.
- Noise injection reduces statistical utility; high privacy budgets (epsilon) may allow inference while low budgets (epsilon <0.1) add significant noise.
- Maintaining k-anonymity becomes harder as dataset grows and rare populations appear; may force conservative suppression of legitimate insights.

### Usage Instructions
1. Identify quasi-identifiers in HR data (age, salary band, department, location, tenure, role). 2. Create aggregation-only views with HAVING COUNT(*) >= 5. 3. Test for k=5 anonymity: SELECT department, role, COUNT(*) FROM employees GROUP BY department, role HAVING COUNT(*) >= 5. 4. For salary analytics, implement noise injection in Python: create base aggregate (SELECT department, avg(salary) as avg_sal FROM employees GROUP BY department), calculate sensitivity (max salary difference), generate Laplace noise with epsilon=0.5, add noise to aggregates. 5. Create security principal with view-only permissions to anonymized views. 6. Publish anonymized views via Power BI semantic model with field-level security. 7. Document epsilon budgets and k values for each published analysis.

### Governance Considerations
> Establish privacy analytics working group with data scientists, privacy officers, and HR stakeholders. Document quasi-identifier sets and privacy threat model per analysis. Set epsilon budgets based on acceptable privacy-utility tradeoff. Review all published aggregates for k-anonymity before release. Track total epsilon consumption across all published analyses to prevent privacy budget exhaustion. Implement technical controls preventing ad-hoc SQL query access to raw employee data.

### People Analytics Use Cases
- Publishing company-wide salary equity analysis to all employees showing average salary by department-level-location, with k=10 minimum group size, enabling transparency without revealing individual salaries.
- Generating anonymized performance distribution histograms for board review with noise injection ensuring no distribution shape discloses individual outliers.
- Creating recruitment funnel analytics published externally showing aggregate conversion rates by source-role with k=5 minimums, preventing inference of individual candidate outcomes.

### Related Patterns
- **Compatible with:** medallion-architecture, row-level-security, dynamic-data-masking, purview-data-map
- **Prerequisites:** medallion-architecture, row-level-security
- **Incompatible with:** None

---

## Audit Log Export and SIEM Integration
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Azure Sentinel, Log Analytics Workspace, Power BI Activity Log, Unified Audit Log, Azure Monitor

### What It Is
Audit log integration ensures all Fabric and Power BI activities (data access, semantic model changes, sharing, export, deletion) are captured, centralized, and analyzed for security incidents. Fabric activity logs (workspace creation, item access, refresh execution, query patterns) flow to Log Analytics Workspace. Power BI activity logs (report view, dataset refresh, sharing changes, export) are forwarded to the Unified Audit Log via the Office 365 Management API. Azure Sentinel consumes these logs, applies correlation rules to detect anomalies (bulk data export, after-hours access, privilege escalation), enriches with identity and threat intelligence, and triggers incidents for SOC investigation. Custom KQL (Kusto Query Language) queries detect HR-specific threats: unusual bulk report exports, access to sensitive employee data by non-HR users, policy violation patterns. Retention ensures logs are available for 1-2 years for forensic analysis and compliance audits.

### Pros
- Centralizes audit logs from Fabric and Power BI in single searchable repository enabling cross-system correlation and forensic investigations.
- Detects insider threats and compliance violations in real-time through rule-based alerting and anomaly detection, enabling rapid response.
- Provides evidence trail for regulatory audits and incident response, meeting SOX, HIPAA, and other audit requirements.

### Cons
- Azure Sentinel ingestion costs scale with log volume; busy Fabric environments can generate 1000+ GB/month of logs, increasing licensing costs.
- Lag between activity and Sentinel processing (typically 1-5 minutes) means real-time detection is limited; historical detection takes longer.
- False positive rates in correlation rules can overwhelm SOC; requires significant tuning and stakeholder coordination.

### Usage Instructions
1. Create Log Analytics Workspace in Azure. 2. Enable Fabric activity logging: Workspace Settings > Audit and Compliance > Enable Activity Logging. 3. Create Data Connector in Log Analytics: Fabric Activity > Diagnostic Settings > Send to Log Analytics Workspace. 4. Enable Power BI audit logging: Power BI Admin Portal > Audit and Compliance > Turn on audit log search. 5. Configure Office 365 Management API in Sentinel to consume Unified Audit Log. 6. In Azure Sentinel, create Data Connectors for Office 365 and Log Analytics. 7. Create KQL detection rules: query for bulk exports (>1000 rows), access to SSN columns, after-hours queries. 8. Configure Incidents from detections with SOAR playbook triggers. 9. Create Power BI dashboard for audit KPIs: daily active users, top data consumers, failed access attempts.

### Governance Considerations
> Establish Security Operations Center (SOC) workflow for Sentinel incidents related to HR data. Define escalation procedures for confirmed security incidents (e.g., data exfiltration). Implement log retention policies: 6 months hot storage, 2 years cold archive. Conduct quarterly reviews of detection rules to reduce false positives. Require formal change management approval for queries accessing sensitive audit data. Ensure audit log access is restricted to security team and select compliance officers.

### People Analytics Use Cases
- Real-time detection of bulk export of executive compensation reports (>100 rows) to external email domains, triggering SOC investigation into potential salary data exfiltration.
- Anomaly detection identifying that a non-HR user (e.g., IT service account) is accessing employee SSN and salary columns during off-hours, indicating potential credential compromise.
- Forensic investigation of a departing manager's last-day activities: queried employee performance data, shared compensation history report with personal email, then deleted workspace link.

### Related Patterns
- **Compatible with:** row-level-security, workspace-permission-governance, dlp-policy-enforcement, privileged-access-management
- **Prerequisites:** None
- **Incompatible with:** None

---

## Data Subject Request Fulfillment Pipeline
**Complexity:** High | **Maturity:** Emerging
**Fabric Components:** Microsoft Purview Data Map, Data Factory Pipeline, OneLake, Fabric Notebooks, Lakehouse

### What It Is
Data Subject Requests (DSR) are formal legal requests from individuals to access (GDPR Article 15) or erase (GDPR Article 17, right-to-be-forgotten) their personal data. Manual DSR handling is error-prone, slow, and costly. Automated DSR fulfillment pipelines use Microsoft Purview Data Map to identify all systems containing an individual's data, orchestrate retrieval or deletion via Data Factory, perform soft-delete in Fabric Lakehouse with audit trail, notify requestor, and verify completion. For HR analytics, DSR requests require identifying employee records across Lakehouse, data warehouse, Power BI datasets, and archived systems. Soft-delete (marking records inactive) enables 30-day appeal period before hard-delete. Lineage mapping shows which analytics and reports are impacted by erasure. Workflow includes validation steps preventing accidental bulk deletion.

### Pros
- Automates time-consuming manual search and deletion, reducing DSR fulfillment time from weeks to days and reducing legal/compliance costs.
- Uses Purview lineage to ensure complete erasure across all systems; manual processes frequently miss copies or derived data.
- Provides audit trail proving compliance with GDPR/PIPEDA deadlines (30 days for access, 30 days for erasure), supporting regulatory defense.

### Cons
- Incomplete or inaccurate Purview Data Map can result in missed data systems and non-compliance; requires continuous curation.
- Soft-delete relies on application logic filtering deleted records; risk of query bugs exposing deleted data if filters are incorrect.
- Determining which analytic derivatives (e.g., aggregates, models, exports) must be updated/deleted is complex and data-dependent.

### Usage Instructions
1. Create DSR request intake form (SharePoint form or Power Apps) capturing: requestor name, email, request type (access/erasure), date. 2. Create Data Factory pipeline: Step 1 - Query Purview Data Map API for assets containing individual's data (e.g., Employee.EmployeeId = 12345). Step 2 - Generate list of impacted systems/tables. Step 3 - For access requests, export data to encrypted file in secure SharePoint. For erasure requests, mark records with is_dsr_deleted=1, log deletion timestamp/reason. Step 4 - Wait 30 days for appeals. Step 5 - Hard-delete (VACUUM, UPDATE DELETE). Step 6 - Notify requestor and compliance team. 7. Implement controls: require approvals for bulk erasure, audit all DSR operations, verify deletion completeness.

### Governance Considerations
> Establish DSR response team with legal, HR, privacy, and data teams. Document DSR procedures and compliance timelines per jurisdiction. Implement technical access controls preventing unauthorized DSR request manipulation. Maintain DSR request audit log with decision and verification steps. Conduct quarterly audits to verify soft-deleted records are truly inaccessible to analytics. Maintain appeal process for 30-day grace period post-deletion request.

### People Analytics Use Cases
- Automated fulfillment of GDPR access request from Canadian employee: Purview identifies data in Lakehouse employee table, warehouse HRIS system, Power BI reports. Pipeline exports to encrypted PDF in 5 days, within GDPR 30-day SLA.
- Right-to-erasure request from terminated EU employee: soft-delete removes from all active tables, historical audit trails remain but employee salary/SSN are masked from all analytics, 30-day appeal period prevents accidental permanent deletion.
- Cross-border DSR for US employee working in EU office: pipeline identifies data in US Lake House capacity (compliant with GDPR data residency because US subject to standard contractual clauses), executes soft-delete with audit trail.

### Related Patterns
- **Compatible with:** purview-data-map, medallion-architecture, audit-siem-integration
- **Prerequisites:** purview-data-map, medallion-architecture
- **Incompatible with:** None

---

## Network Isolation with Private Endpoints
**Complexity:** High | **Maturity:** GA
**Fabric Components:** Azure Private Link, Azure VNet, Managed Private Endpoints, Fabric Capacity

### What It Is
Private Endpoints eliminate internet routes for Fabric services, instead routing all traffic through Azure VNet private network. Fabric Capacity (compute and storage) uses Private Endpoints to ensure no data traverses public internet. Managed Private Endpoints for Spark Compute enable secure communication with private data sources (SQL Database in VNet, storage accounts with firewall enabled). For HR analytics in regulated environments (financial services, healthcare), network isolation ensures employee data never transits public internet. Network security groups (NSGs) can further restrict traffic by source/destination IP. VNet integration enables hybrid connectivity: on-premises HR systems can securely connect to Fabric via ExpressRoute. Outbound traffic can be forced through proxy/firewall for inspection. Azure Private Link services provide 99.99% availability.

### Pros
- Eliminates internet exposure of Fabric endpoints, significantly reducing attack surface and complying with network isolation requirements.
- Enables hybrid connectivity to on-premises systems without VPN, improving performance and security.
- Provides network-layer segmentation complementing identity and data-layer security controls, following defense-in-depth principle.

### Cons
- Private Endpoints add operational complexity: VNet design, routing, DNS configuration, and troubleshooting require network expertise.
- Cost increases: Fabric Capacity pricing unchanged but Private Endpoints charge $0.50/hour per endpoint, adding $360/month per capacity.
- Hybrid connectivity requires ExpressRoute or Site-to-Site VPN; on-premises connectivity adds complexity and latency.

### Usage Instructions
1. Create Azure VNet in the same region as Fabric Capacity. 2. In Fabric Workspace Settings, enable Private Endpoints: select Capacity > Network > Enable Private Endpoint. 3. Azure creates Private Link Service and provides Private Endpoint Connection. 4. In your VNet, create Private Endpoint resource: +Create > Private Endpoint, select Fabric service, select subnet, configure DNS integration. 5. Update DNS resolver to map fabric.microsoft.com to private IP (e.g., 10.0.0.5). 6. Test connectivity: connect VM in VNet, query nslookup fabric.microsoft.com (should resolve to private IP). 7. Configure Managed Private Endpoints for Spark: Workspace > Managed Private Endpoints > +New, select target resource (SQL Database, storage), approve in target resource. 8. Configure Network Security Group (NSG): allow only VNet subnets to reach Fabric Private Endpoint, deny internet-routed traffic.

### Governance Considerations
> Establish network security architecture review with IT security and compliance teams. Document VNet design and Private Endpoint locations. Implement bastion hosts for secure VM access instead of public IPs. Enforce NSG rules preventing traffic to public internet. Monitor Private Endpoint connections and deny suspicious outbound attempts. Require change management approval for VNet/NSG changes. Conduct quarterly network segmentation audits.

### People Analytics Use Cases
- Financial services firm isolates HR analytics Fabric Capacity on private VNet, restricts outbound traffic to approved SIEM sink via proxy, ensuring no employee data transits internet.
- Healthcare provider connects on-premises HRIS system via ExpressRoute to Fabric over private endpoint, enabling analytics without routing PII through public internet or VPN.
- Multi-tenant SaaS provider isolates each customer's Fabric Capacity on separate VNet, using managed private endpoints to connect to customer-specific SQL databases on-premises.

### Related Patterns
- **Compatible with:** encryption-at-rest-cmk, workspace-permission-governance, audit-siem-integration
- **Prerequisites:** None
- **Incompatible with:** None

---

## Just-in-Time Privileged Access Management
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Azure Entra ID PIM, Fabric Workspace Roles, Azure Key Vault, Azure Sentinel

### What It Is
Privileged Identity Management (PIM) reduces standing permissions, requiring users to request temporary elevation to admin roles. For HR analytics, workspace admins manage data governance policies, sharing, and sensitive configurations. Rather than making users permanent admins (standing privilege), PIM makes them 'Eligible Admins' who must request activation. Requests require approval from compliance officer and MFA authentication. Activation is time-limited (1-8 hours) and audited. Break-glass emergency accounts provide fallback access if primary admins are unavailable. Multi-factor authentication (MFA) is required for all privileged actions. Audit logs in Entra ID capture all activation requests, approvals, and actions performed during elevated access. For compliance, PIM demonstrates least-privilege principle and immediate detection of unauthorized privilege escalation attempts.

### Pros
- Reduces standing privilege, dramatically lowering risk of compromise: admin account hack affects only active activation window (1-8 hours) not 365 days.
- Requires approval for every elevation, creating human checkpoint preventing unauthorized access.
- Complete audit trail of privilege escalation enables detection of unusual elevation patterns and supports compliance audits.

### Cons
- PIM adds friction to emergency access scenarios, requiring approval workflow adds 15-30 minutes to incident response.
- Admin users must have Entra ID Premium P2 license, adding cost ~$30-50/user/month.
- Misconfigured break-glass accounts (credentials leaked, not rotated) undermine PIM's security benefits.

### Usage Instructions
1. Ensure Entra ID Premium P2 licensed. 2. In Entra ID > Privileged Identity Management > Fabric Workspace Roles, select 'Workspace Admin' role. 3. Set eligible users: add workspace managers as Eligible (not Permanent) members. 4. Configure activation: require approval, require MFA, set max activation duration to 4 hours. 5. Select approval delegator: compliance officer or security team. 6. Configure notifications: alert on elevations, email approvers. 7. Create break-glass account: dedicate account for emergency access, store credentials in physical safe (not digital). 8. Test activation: Eligible Admin requests activation, approver receives email, activates with MFA. 9. Monitor in Azure Sentinel: create alert for approval denials, unusual activation times, after-hours elevations. 10. Quarterly review: audit PIM logs, revoke unused eligible access.

### Governance Considerations
> Establish PIM governance committee with security, HR, and compliance stakeholders. Document approval process and SLA for activation requests (should be <15 minutes). Implement technical controls enforcing MFA (hardware keys preferred). Rotate break-glass credentials quarterly with multiple stakeholders witnessing. Test break-glass emergency access annually. Review PIM logs monthly for suspicious patterns. Enforce organization-wide policy: no permanent privileged roles, all admins must use PIM.

### People Analytics Use Cases
- HR analytics workspace admin (normally ineligible) requests elevation to investigate unauthorized data export, approver grants 4-hour activation via MFA approval, admin investigates access logs with limited time window.
- Data governance officer regularly activates to review sensitivity label assignments and RLS policies, must approve each activation with business justification.
- Emergency incident: production Fabric capacity is down, break-glass account holder activates with MFA, gains temporary admin access to restart services, audited and revoked within 1 hour.

### Related Patterns
- **Compatible with:** workspace-permission-governance, audit-siem-integration, encryption-at-rest-cmk
- **Prerequisites:** None
- **Incompatible with:** None

---

## Encryption at Rest with Customer-Managed Keys
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Azure Key Vault, OneLake, Fabric Workspace Settings, Entra ID Service Principal

### What It Is
Customer-Managed Key (CMK) encryption provides organizational control over encryption key lifecycle and rotation. In financial services HR analytics, CMK encryption via Azure Key Vault ensures that OneLake workspace data is encrypted with keys managed by your organization, not Microsoft. All data in transit uses TLS 1.2 or higher. This approach meets regulatory requirements for key custody, enables key rotation policies, supports audit logging for key access, and provides compliance with FIPS 140-2 standards for handling highly sensitive employee financial and personal data. Integration with Entra ID service principals allows role-based access control over decryption operations.

### Pros
- Provides organizational control over encryption keys with full audit trail of key access and rotations.
- Enables compliance with regulations requiring customer-managed encryption (SOX, GDPR, PIPEDA, HIPAA).
- Supports break-glass emergency key access protocols and disaster recovery scenarios.

### Cons
- Increases operational complexity requiring key rotation and lifecycle management procedures.
- Key Vault service calls add latency to Fabric operations, typically <10ms but noticeable at scale.
- Requires careful IAM design to prevent accidental key lockout that could make data unrecoverable.

### Usage Instructions
1. Create an Azure Key Vault resource in the same region as Fabric capacity. 2. Generate RSA 3072-bit or 4096-bit CMK in Key Vault. 3. Grant Fabric capacity system-assigned managed identity Key Wrap/Unwrap permissions on the key. 4. In Fabric Workspace Settings, select 'Customer Managed Key' and specify the Key Vault URI. 5. Configure key rotation policy (annual minimum). 6. Enable Key Vault audit logging and monitor access. 7. Test disaster recovery failover procedures quarterly.

### Governance Considerations
> Establish a key management committee with business and security stakeholders. Document key rotation procedures and emergency access protocols. Implement access reviews quarterly for Key Vault permissions. Ensure backup keys are stored in a geographically separate region. Monitor failed decryption attempts and investigate anomalies. Integrate key rotation events into change management processes.

### People Analytics Use Cases
- Salary survey analysis where payroll data is encrypted with organization-controlled CMK, enabling internal audits while maintaining key custody.
- Executive compensation dashboards requiring SOX compliance where CMK encryption demonstrates regulatory control over sensitive executive personal data.
- International employee equity tracking where Canadian employee data uses Canadian Key Vault instance and US data uses US Key Vault for data residency compliance.

### Related Patterns
- **Compatible with:** sensitivity-labels, purview-data-map, dynamic-data-masking, row-level-security
- **Prerequisites:** None
- **Incompatible with:** None

---

## Data Loss Prevention Policy Enforcement
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Microsoft Purview DLP, Sensitivity Labels, Power BI, OneLake

### What It Is
Data Loss Prevention (DLP) policies in Microsoft Purview automatically detect sensitive information types within Fabric and Power BI, then enforce preventive or detective controls. For HR analytics, DLP policies identify patterns matching US Social Security Numbers, salary ranges, employee IDs, and bank account numbers. When detected, policies can block exports to CSV/Excel, prevent uploads to personal OneDrive, restrict sharing to external domains, require approval for sensitive queries, or log incidents to Azure Sentinel for SOC review. DLP works alongside sensitivity labels to provide multi-layered protection. Policies can be scoped to specific workspaces, datasets, or semantic models. Integration with Sensitivity Labels and Power BI Workspace settings ensures consistent enforcement across analytics surfaces.

### Pros
- Detects sensitive data automatically using built-in and custom regex patterns without manual classification.
- Blocks unauthorized export at the point of action (export, copy, print) reducing insider threat risk.
- Provides audit trail of blocked/allowed actions and integrates with SIEM for incident response workflows.

### Cons
- Can trigger false positives on benign data patterns, requiring regular tuning and user exceptions.
- DLP policies are primarily detective in Power BI; preventive enforcement requires specific workspace integration.
- Regex patterns for custom sensitive data types require security team expertise and ongoing maintenance.

### Usage Instructions
1. Open Microsoft Purview Compliance Center and navigate to Data Loss Prevention > Policies. 2. Create new policy with template 'Financial Info' or 'PII' as baseline. 3. Add custom sensitive info types: SSN regex (^\\d{3}-\\d{2}-\\d{4}$), salary range (\\$[0-9]{3,4}[KM]). 4. Configure rule actions: 'Restrict access' for Power BI, 'Require justification' for exports, 'Send alert to admin'. 5. Set policy scope to HR workspace and datasets. 6. Enable incident reporting to Azure Sentinel. 7. Test policy with sample data before production rollout. 8. Review blocked incidents monthly.

### Governance Considerations
> Establish a DLP governance committee with HR, security, and legal teams. Document all custom sensitive data type patterns and business justification. Implement exception request workflow with business and compliance approval. Monitor false positive rate and adjust thresholds quarterly. Ensure DLP incidents are correlated with user access logs and audit trails. Train HR analytics team on compliant export procedures.

### People Analytics Use Cases
- Automated blocking of salary equity analysis exports containing aggregated ranges to unauthorized recipients, while allowing HR team to export to approved HR department network shares.
- Detection and alert when employee benefit election data containing SSN is copied to clipboard or exported to personal email, triggering incident response investigation.
- Prevention of executive compensation dashboard drill-through exports to external consultants without pre-approval workflow, enforcing approval for sensitive roles.

### Related Patterns
- **Compatible with:** sensitivity-labels, row-level-security, dynamic-data-masking, audit-siem-integration
- **Prerequisites:** sensitivity-labels
- **Incompatible with:** None

---

## Statistical Anonymization for HR Analytics
**Complexity:** High | **Maturity:** Emerging
**Fabric Components:** Fabric Warehouse, SQL Analytics Endpoint, PySpark Notebooks, Lakehouse

### What It Is
K-anonymity ensures that any combination of quasi-identifiers (age, department, salary band) appears in at least k records, preventing record linkage attacks. Differential privacy adds carefully calibrated noise to query results, enabling accurate aggregate statistics while preventing inference of individual values. For HR analytics, aggregation-only views enforce k-anonymity by requiring HAVING COUNT(*) >= 5 clauses on all queries, preventing disclosure of rare populations (e.g., the sole executive in a location). Noise injection adds Laplace or Gaussian noise proportional to sensitivity, with epsilon (privacy budget) controlling noise magnitude. Views in Fabric Warehouse or SQL Analytics Endpoint implement these controls. PySpark notebooks implement noise injection for ad-hoc analyses. Practical applications include publishing salary bands by role (not individuals), showing headcount by department (minimum 5 per group), and publishing engagement scores by location-function groups.

### Pros
- Provides formal mathematical guarantees against re-identification attacks, meeting GDPR and other privacy regulations' proportionality requirements.
- Enables publishing aggregate HR analytics to broad audiences (all employees, board, public) without risk of individual inference.
- Can be implemented as database views and functions, integrating seamlessly into existing analytics without changing consuming applications.

### Cons
- K-anonymity vulnerable to semantic attacks if quasi-identifiers are not carefully chosen; requires domain expertise to identify all identifying combinations.
- Noise injection reduces statistical utility; high privacy budgets (epsilon) may allow inference while low budgets (epsilon <0.1) add significant noise.
- Maintaining k-anonymity becomes harder as dataset grows and rare populations appear; may force conservative suppression of legitimate insights.

### Usage Instructions
1. Identify quasi-identifiers in HR data (age, salary band, department, location, tenure, role). 2. Create aggregation-only views with HAVING COUNT(*) >= 5. 3. Test for k=5 anonymity: SELECT department, role, COUNT(*) FROM employees GROUP BY department, role HAVING COUNT(*) >= 5. 4. For salary analytics, implement noise injection in Python: create base aggregate (SELECT department, avg(salary) as avg_sal FROM employees GROUP BY department), calculate sensitivity (max salary difference), generate Laplace noise with epsilon=0.5, add noise to aggregates. 5. Create security principal with view-only permissions to anonymized views. 6. Publish anonymized views via Power BI semantic model with field-level security. 7. Document epsilon budgets and k values for each published analysis.

### Governance Considerations
> Establish privacy analytics working group with data scientists, privacy officers, and HR stakeholders. Document quasi-identifier sets and privacy threat model per analysis. Set epsilon budgets based on acceptable privacy-utility tradeoff. Review all published aggregates for k-anonymity before release. Track total epsilon consumption across all published analyses to prevent privacy budget exhaustion. Implement technical controls preventing ad-hoc SQL query access to raw employee data.

### People Analytics Use Cases
- Publishing company-wide salary equity analysis to all employees showing average salary by department-level-location, with k=10 minimum group size, enabling transparency without revealing individual salaries.
- Generating anonymized performance distribution histograms for board review with noise injection ensuring no distribution shape discloses individual outliers.
- Creating recruitment funnel analytics published externally showing aggregate conversion rates by source-role with k=5 minimums, preventing inference of individual candidate outcomes.

### Related Patterns
- **Compatible with:** medallion-architecture, row-level-security, dynamic-data-masking, purview-data-map
- **Prerequisites:** medallion-architecture, row-level-security
- **Incompatible with:** None

---

## Audit Log Export and SIEM Integration
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Azure Sentinel, Log Analytics Workspace, Power BI Activity Log, Unified Audit Log, Azure Monitor

### What It Is
Audit log integration ensures all Fabric and Power BI activities (data access, semantic model changes, sharing, export, deletion) are captured, centralized, and analyzed for security incidents. Fabric activity logs (workspace creation, item access, refresh execution, query patterns) flow to Log Analytics Workspace. Power BI activity logs (report view, dataset refresh, sharing changes, export) are forwarded to the Unified Audit Log via the Office 365 Management API. Azure Sentinel consumes these logs, applies correlation rules to detect anomalies (bulk data export, after-hours access, privilege escalation), enriches with identity and threat intelligence, and triggers incidents for SOC investigation. Custom KQL (Kusto Query Language) queries detect HR-specific threats: unusual bulk report exports, access to sensitive employee data by non-HR users, policy violation patterns. Retention ensures logs are available for 1-2 years for forensic analysis and compliance audits.

### Pros
- Centralizes audit logs from Fabric and Power BI in single searchable repository enabling cross-system correlation and forensic investigations.
- Detects insider threats and compliance violations in real-time through rule-based alerting and anomaly detection, enabling rapid response.
- Provides evidence trail for regulatory audits and incident response, meeting SOX, HIPAA, and other audit requirements.

### Cons
- Azure Sentinel ingestion costs scale with log volume; busy Fabric environments can generate 1000+ GB/month of logs, increasing licensing costs.
- Lag between activity and Sentinel processing (typically 1-5 minutes) means real-time detection is limited; historical detection takes longer.
- False positive rates in correlation rules can overwhelm SOC; requires significant tuning and stakeholder coordination.

### Usage Instructions
1. Create Log Analytics Workspace in Azure. 2. Enable Fabric activity logging: Workspace Settings > Audit and Compliance > Enable Activity Logging. 3. Create Data Connector in Log Analytics: Fabric Activity > Diagnostic Settings > Send to Log Analytics Workspace. 4. Enable Power BI audit logging: Power BI Admin Portal > Audit and Compliance > Turn on audit log search. 5. Configure Office 365 Management API in Sentinel to consume Unified Audit Log. 6. In Azure Sentinel, create Data Connectors for Office 365 and Log Analytics. 7. Create KQL detection rules: query for bulk exports (>1000 rows), access to SSN columns, after-hours queries. 8. Configure Incidents from detections with SOAR playbook triggers. 9. Create Power BI dashboard for audit KPIs: daily active users, top data consumers, failed access attempts.

### Governance Considerations
> Establish Security Operations Center (SOC) workflow for Sentinel incidents related to HR data. Define escalation procedures for confirmed security incidents (e.g., data exfiltration). Implement log retention policies: 6 months hot storage, 2 years cold archive. Conduct quarterly reviews of detection rules to reduce false positives. Require formal change management approval for queries accessing sensitive audit data. Ensure audit log access is restricted to security team and select compliance officers.

### People Analytics Use Cases
- Real-time detection of bulk export of executive compensation reports (>100 rows) to external email domains, triggering SOC investigation into potential salary data exfiltration.
- Anomaly detection identifying that a non-HR user (e.g., IT service account) is accessing employee SSN and salary columns during off-hours, indicating potential credential compromise.
- Forensic investigation of a departing manager's last-day activities: queried employee performance data, shared compensation history report with personal email, then deleted workspace link.

### Related Patterns
- **Compatible with:** row-level-security, workspace-permission-governance, dlp-policy-enforcement, privileged-access-management
- **Prerequisites:** None
- **Incompatible with:** None

---

## Data Subject Request Fulfillment Pipeline
**Complexity:** High | **Maturity:** Emerging
**Fabric Components:** Microsoft Purview Data Map, Data Factory Pipeline, OneLake, Fabric Notebooks, Lakehouse

### What It Is
Data Subject Requests (DSR) are formal legal requests from individuals to access (GDPR Article 15) or erase (GDPR Article 17, right-to-be-forgotten) their personal data. Manual DSR handling is error-prone, slow, and costly. Automated DSR fulfillment pipelines use Microsoft Purview Data Map to identify all systems containing an individual's data, orchestrate retrieval or deletion via Data Factory, perform soft-delete in Fabric Lakehouse with audit trail, notify requestor, and verify completion. For HR analytics, DSR requests require identifying employee records across Lakehouse, data warehouse, Power BI datasets, and archived systems. Soft-delete (marking records inactive) enables 30-day appeal period before hard-delete. Lineage mapping shows which analytics and reports are impacted by erasure. Workflow includes validation steps preventing accidental bulk deletion.

### Pros
- Automates time-consuming manual search and deletion, reducing DSR fulfillment time from weeks to days and reducing legal/compliance costs.
- Uses Purview lineage to ensure complete erasure across all systems; manual processes frequently miss copies or derived data.
- Provides audit trail proving compliance with GDPR/PIPEDA deadlines (30 days for access, 30 days for erasure), supporting regulatory defense.

### Cons
- Incomplete or inaccurate Purview Data Map can result in missed data systems and non-compliance; requires continuous curation.
- Soft-delete relies on application logic filtering deleted records; risk of query bugs exposing deleted data if filters are incorrect.
- Determining which analytic derivatives (e.g., aggregates, models, exports) must be updated/deleted is complex and data-dependent.

### Usage Instructions
1. Create DSR request intake form (SharePoint form or Power Apps) capturing: requestor name, email, request type (access/erasure), date. 2. Create Data Factory pipeline: Step 1 - Query Purview Data Map API for assets containing individual's data (e.g., Employee.EmployeeId = 12345). Step 2 - Generate list of impacted systems/tables. Step 3 - For access requests, export data to encrypted file in secure SharePoint. For erasure requests, mark records with is_dsr_deleted=1, log deletion timestamp/reason. Step 4 - Wait 30 days for appeals. Step 5 - Hard-delete (VACUUM, UPDATE DELETE). Step 6 - Notify requestor and compliance team. 7. Implement controls: require approvals for bulk erasure, audit all DSR operations, verify deletion completeness.

### Governance Considerations
> Establish DSR response team with legal, HR, privacy, and data teams. Document DSR procedures and compliance timelines per jurisdiction. Implement technical access controls preventing unauthorized DSR request manipulation. Maintain DSR request audit log with decision and verification steps. Conduct quarterly audits to verify soft-deleted records are truly inaccessible to analytics. Maintain appeal process for 30-day grace period post-deletion request.

### People Analytics Use Cases
- Automated fulfillment of GDPR access request from Canadian employee: Purview identifies data in Lakehouse employee table, warehouse HRIS system, Power BI reports. Pipeline exports to encrypted PDF in 5 days, within GDPR 30-day SLA.
- Right-to-erasure request from terminated EU employee: soft-delete removes from all active tables, historical audit trails remain but employee salary/SSN are masked from all analytics, 30-day appeal period prevents accidental permanent deletion.
- Cross-border DSR for US employee working in EU office: pipeline identifies data in US Lake House capacity (compliant with GDPR data residency because US subject to standard contractual clauses), executes soft-delete with audit trail.

### Related Patterns
- **Compatible with:** purview-data-map, medallion-architecture, audit-siem-integration
- **Prerequisites:** purview-data-map, medallion-architecture
- **Incompatible with:** None

---

## Network Isolation with Private Endpoints
**Complexity:** High | **Maturity:** GA
**Fabric Components:** Azure Private Link, Azure VNet, Managed Private Endpoints, Fabric Capacity

### What It Is
Private Endpoints eliminate internet routes for Fabric services, instead routing all traffic through Azure VNet private network. Fabric Capacity (compute and storage) uses Private Endpoints to ensure no data traverses public internet. Managed Private Endpoints for Spark Compute enable secure communication with private data sources (SQL Database in VNet, storage accounts with firewall enabled). For HR analytics in regulated environments (financial services, healthcare), network isolation ensures employee data never transits public internet. Network security groups (NSGs) can further restrict traffic by source/destination IP. VNet integration enables hybrid connectivity: on-premises HR systems can securely connect to Fabric via ExpressRoute. Outbound traffic can be forced through proxy/firewall for inspection. Azure Private Link services provide 99.99% availability.

### Pros
- Eliminates internet exposure of Fabric endpoints, significantly reducing attack surface and complying with network isolation requirements.
- Enables hybrid connectivity to on-premises systems without VPN, improving performance and security.
- Provides network-layer segmentation complementing identity and data-layer security controls, following defense-in-depth principle.

### Cons
- Private Endpoints add operational complexity: VNet design, routing, DNS configuration, and troubleshooting require network expertise.
- Cost increases: Fabric Capacity pricing unchanged but Private Endpoints charge $0.50/hour per endpoint, adding $360/month per capacity.
- Hybrid connectivity requires ExpressRoute or Site-to-Site VPN; on-premises connectivity adds complexity and latency.

### Usage Instructions
1. Create Azure VNet in the same region as Fabric Capacity. 2. In Fabric Workspace Settings, enable Private Endpoints: select Capacity > Network > Enable Private Endpoint. 3. Azure creates Private Link Service and provides Private Endpoint Connection. 4. In your VNet, create Private Endpoint resource: +Create > Private Endpoint, select Fabric service, select subnet, configure DNS integration. 5. Update DNS resolver to map fabric.microsoft.com to private IP (e.g., 10.0.0.5). 6. Test connectivity: connect VM in VNet, query nslookup fabric.microsoft.com (should resolve to private IP). 7. Configure Managed Private Endpoints for Spark: Workspace > Managed Private Endpoints > +New, select target resource (SQL Database, storage), approve in target resource. 8. Configure Network Security Group (NSG): allow only VNet subnets to reach Fabric Private Endpoint, deny internet-routed traffic.

### Governance Considerations
> Establish network security architecture review with IT security and compliance teams. Document VNet design and Private Endpoint locations. Implement bastion hosts for secure VM access instead of public IPs. Enforce NSG rules preventing traffic to public internet. Monitor Private Endpoint connections and deny suspicious outbound attempts. Require change management approval for VNet/NSG changes. Conduct quarterly network segmentation audits.

### People Analytics Use Cases
- Financial services firm isolates HR analytics Fabric Capacity on private VNet, restricts outbound traffic to approved SIEM sink via proxy, ensuring no employee data transits internet.
- Healthcare provider connects on-premises HRIS system via ExpressRoute to Fabric over private endpoint, enabling analytics without routing PII through public internet or VPN.
- Multi-tenant SaaS provider isolates each customer's Fabric Capacity on separate VNet, using managed private endpoints to connect to customer-specific SQL databases on-premises.

### Related Patterns
- **Compatible with:** encryption-at-rest-cmk, workspace-permission-governance, audit-siem-integration
- **Prerequisites:** None
- **Incompatible with:** None

---

## Just-in-Time Privileged Access Management
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Azure Entra ID PIM, Fabric Workspace Roles, Azure Key Vault, Azure Sentinel

### What It Is
Privileged Identity Management (PIM) reduces standing permissions, requiring users to request temporary elevation to admin roles. For HR analytics, workspace admins manage data governance policies, sharing, and sensitive configurations. Rather than making users permanent admins (standing privilege), PIM makes them 'Eligible Admins' who must request activation. Requests require approval from compliance officer and MFA authentication. Activation is time-limited (1-8 hours) and audited. Break-glass emergency accounts provide fallback access if primary admins are unavailable. Multi-factor authentication (MFA) is required for all privileged actions. Audit logs in Entra ID capture all activation requests, approvals, and actions performed during elevated access. For compliance, PIM demonstrates least-privilege principle and immediate detection of unauthorized privilege escalation attempts.

### Pros
- Reduces standing privilege, dramatically lowering risk of compromise: admin account hack affects only active activation window (1-8 hours) not 365 days.
- Requires approval for every elevation, creating human checkpoint preventing unauthorized access.
- Complete audit trail of privilege escalation enables detection of unusual elevation patterns and supports compliance audits.

### Cons
- PIM adds friction to emergency access scenarios, requiring approval workflow adds 15-30 minutes to incident response.
- Admin users must have Entra ID Premium P2 license, adding cost ~$30-50/user/month.
- Misconfigured break-glass accounts (credentials leaked, not rotated) undermine PIM's security benefits.

### Usage Instructions
1. Ensure Entra ID Premium P2 licensed. 2. In Entra ID > Privileged Identity Management > Fabric Workspace Roles, select 'Workspace Admin' role. 3. Set eligible users: add workspace managers as Eligible (not Permanent) members. 4. Configure activation: require approval, require MFA, set max activation duration to 4 hours. 5. Select approval delegator: compliance officer or security team. 6. Configure notifications: alert on elevations, email approvers. 7. Create break-glass account: dedicate account for emergency access, store credentials in physical safe (not digital). 8. Test activation: Eligible Admin requests activation, approver receives email, activates with MFA. 9. Monitor in Azure Sentinel: create alert for approval denials, unusual activation times, after-hours elevations. 10. Quarterly review: audit PIM logs, revoke unused eligible access.

### Governance Considerations
> Establish PIM governance committee with security, HR, and compliance stakeholders. Document approval process and SLA for activation requests (should be <15 minutes). Implement technical controls enforcing MFA (hardware keys preferred). Rotate break-glass credentials quarterly with multiple stakeholders witnessing. Test break-glass emergency access annually. Review PIM logs monthly for suspicious patterns. Enforce organization-wide policy: no permanent privileged roles, all admins must use PIM.

### People Analytics Use Cases
- HR analytics workspace admin (normally ineligible) requests elevation to investigate unauthorized data export, approver grants 4-hour activation via MFA approval, admin investigates access logs with limited time window.
- Data governance officer regularly activates to review sensitivity label assignments and RLS policies, must approve each activation with business justification.
- Emergency incident: production Fabric capacity is down, break-glass account holder activates with MFA, gains temporary admin access to restart services, audited and revoked within 1 hour.

### Related Patterns
- **Compatible with:** workspace-permission-governance, audit-siem-integration, encryption-at-rest-cmk
- **Prerequisites:** None
- **Incompatible with:** None

---

