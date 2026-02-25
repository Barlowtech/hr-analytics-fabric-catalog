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

