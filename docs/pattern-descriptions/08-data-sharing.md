# Data Sharing and Collaboration

Modern HR analytics platforms don't exist in isolation; they need to share data securely with partners, other
departments, and external systems. This domain covers patterns for implementing secure data sharing, managing data partnerships,
and collaborating across organizational boundaries.

These patterns address the challenge of maintaining security and governance while enabling the collaboration necessary for
comprehensive people analytics. They cover both internal sharing (cross-departmental access to HR insights) and external sharing
(with vendors, consultants, or partner organizations).

Effective data sharing patterns build trust, accelerate collaboration, and enable HR analytics to contribute to broader
organizational initiatives while protecting sensitive employee information.

---

## Cross-Workspace Data Sharing via Shortcuts
**Complexity:** Low | **Maturity:** GA
**Fabric Components:** OneLake, Shortcuts, Workspaces

### What It Is
Finance workspace has authoritative employee master and cost centers. HR and Recruiting create shortcuts, always get latest data.

### Pros
- Single source of truth.
- Zero-copy sharing.
- Automatic updates visible.

### Cons
- Cross-workspace latency.
- Complex ownership management.
- Lineage harder to track.

### Usage Instructions
1. Source workspace has data. 2. Consumer workspace creates shortcut. 3. Reference shortcut like local table. 4. Monitor performance.

### Governance Considerations
> Source table ownership clear. Data contracts documented. Shortcut access controlled. Performance monitored.

### People Analytics Use Cases
- Finance employee master shared to HR via shortcuts.
- Recruiting access cost center via Finance shortcut.
- All teams access central org structure.

### Related Patterns
- **Compatible with:** onelake-shortcuts, hub-spoke-workspace
- **Prerequisites:** None
- **Incompatible with:** None

---

## Cross-Tenant Data Sharing (B2B Scenarios)
**Complexity:** High | **Maturity:** Preview
**Fabric Components:** OneLake, Shortcuts, Tenants, Azure AD

### What It Is
Parent company shares org structure and benchmark data with subsidiary. Subsidiary accesses via external shortcuts securely.

### Pros
- Enables partner collaboration.
- Maintains security across tenants.
- Zero-copy for cross-tenant data.

### Cons
- Complex permission management.
- Cross-tenant latency.
- Requires Azure AD trust.

### Usage Instructions
1. Source tenant grants access. 2. Target tenant creates shortcut. 3. Authenticate across tenants. 4. Reference shortcut.

### Governance Considerations
> Explicit cross-tenant contracts. Legal agreements. Access regularly reviewed. Sensitive data restricted.

### People Analytics Use Cases
- Parent company shares benchmarks with subsidiary.
- Shared services org shares data with business units.
- JV shares hiring data with partners.

### Related Patterns
- **Compatible with:** onelake-shortcuts
- **Prerequisites:** None
- **Incompatible with:** None

---

## Semantic Model Certification Pipeline
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Semantic Model, Power BI, CI/CD, Approval Workflow

### What It Is
Data team publishes employee dimension model. BI team runs tests, checks metadata, certifies if passed. Analysts use certified models.

### Pros
- Ensures semantic model quality.
- Reduces model duplication.
- Governance automation.

### Cons
- Slows model time-to-value.
- Certification bottleneck.
- Requires clear criteria.

### Usage Instructions
1. Data team publishes model. 2. Auto-run quality checks. 3. BI team reviews. 4. Approve/reject. 5. Publish as Certified. 6. Analysts use.

### Governance Considerations
> Certification criteria clear. Review time SLA defined. Criteria version controlled. Regular audit of certified models.

### People Analytics Use Cases
- Employee dimension certification before BI use.
- Payroll semantic model certification.
- Org structure model quality gates.
- Metrics model certification.

### Related Patterns
- **Compatible with:** certified-semantic-model, deployment-pipelines
- **Prerequisites:** None
- **Incompatible with:** None

---

## REST API Exposure and Management
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Warehouse, SQL Endpoints, API Management, REST API

### What It Is
REST API endpoints for employee master, org structure, payroll data. External HRIS calls API to fetch org updates. Managed API throttling.

### Pros
- Programmatic data access.
- Enables external integrations.
- API governance and throttling.
- Reduces data replication.

### Cons
- API security overhead.
- Performance tuning needed.
- Version management complexity.

### Usage Instructions
1. Create API Management instance. 2. Expose Warehouse via API. 3. Define endpoints. 4. Set throttling. 5. Manage keys. 6. Monitor usage.

### Governance Considerations
> API authentication required. Rate limiting enforced. Data access logged. Sensitive data restricted at API level.

### People Analytics Use Cases
- API for employee master to external HRIS.
- Org structure API to recruiting platforms.
- Payroll data API to finance systems.
- Compensation band API to offer letter system.

### Related Patterns
- **Compatible with:** lakehouse-warehouse-selection, row-level-security
- **Prerequisites:** None
- **Incompatible with:** None

---

## Dataset Subscription and Change Alerts
**Complexity:** Medium | **Maturity:** Preview
**Fabric Components:** Event Grid, Webhooks, Lakehouse, Subscribers

### What It Is
Recruiting platform subscribes to org structure changes. When org structure table updates, recruiting system receives alert, refetches data.

### Pros
- Push-based data distribution.
- Subscribers notified of changes.
- Reduces polling.
- Real-time integration.

### Cons
- Webhook management overhead.
- Failure handling complexity.
- Debugging integration issues.

### Usage Instructions
1. Configure Event Grid. 2. Define dataset change events. 3. Create webhooks for subscribers. 4. Subscribers listen. 5. Notify on change. 6. Handle failures.

### Governance Considerations
> Subscription management. Event audit trail. Webhook security. Retry policies defined.

### People Analytics Use Cases
- Org structure change alerts to recruiting system.
- Employee master update alerts to payroll.
- Compensation change alerts to benefits system.
- Headcount change alerts to planning tools.

### Related Patterns
- **Compatible with:** medallion-architecture, data-activator-reflex
- **Prerequisites:** None
- **Incompatible with:** None

---

## Disaster Recovery and Geo-Redundancy
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** OneLake, Fabric Capacity, Azure Region Pairs, Zone-Redundant Storage

### What It Is
Disaster recovery ensures business continuity when regional outages occur. OneLake Zone-Redundant Storage (ZRS) replicates data across three availability zones within a region, protecting against zone-level failures. Geo-replication asynchronously copies data to a paired region (e.g., US East 2 to US Central 1), protecting against regional disasters. Fabric Capacity can be provisioned in multiple regions to enable manual failover. For HR analytics, disaster recovery ensures employee data is always available and compliant with data residency laws (e.g., Canadian data stays in Canada region). Multi-geo capacity configuration enables capacity to be deployed in specific regions. Backup procedures include daily snapshots exported to secure storage. Manual failover involves updating connection strings and repointing workspaces to failover capacity in alternate region. Recovery Time Objective (RTO) for manual failover is 4-8 hours; automated failover via service mesh future capability targets RTO <15 minutes.

### Pros
- ZRS provides automatic replication without application changes, protecting against zone and data center failures with no additional cost.
- Geo-replication enables regional compliance (e.g., Canadian data in Canada) and disaster recovery to another region, meeting business continuity SLAs.
- Manual failover procedures are tested and documented, enabling rapid recovery with minimal training.

### Cons
- Geo-replication introduces asynchronous delay (minutes to hours); recent data changes may not be replicated if failover occurs immediately after write.
- Manual failover requires human action and coordination, typically taking 4-8 hours; automated failover is not yet available.
- Multi-region Fabric Capacity costs increase significantly; maintaining hot-hot failover doubles capacity costs vs. cold standby.

### Usage Instructions
1. Enable ZRS on OneLake workspace: Workspace Settings > Storage Redundancy > Zone-Redundant Storage. 2. Configure geo-replication: Workspace Settings > Disaster Recovery > Enable Geo-Replication to paired region (e.g., East 2 to Central 1). 3. Create Data Factory pipeline for daily snapshot export: copy all Lakehouse tables to Azure Storage Account in alternate region. 4. Document failover runbook: 1) Declare disaster, 2) Notify stakeholders, 3) Verify failover region readiness, 4) Update Fabric workspace connection to failover capacity, 5) Repoint Power BI datasets to failover semantic models, 6) Validate data integrity in failover region. 5. Conduct quarterly disaster recovery drill: simulate regional failure, execute failover, validate analytics in alternate region, measure RTO. 6. Maintain failover capacity in standby mode or scale down when not in use.

### Governance Considerations
> Establish disaster recovery committee with IT, business continuity, and HR stakeholders. Define RTO (Recovery Time Objective) and RPO (Recovery Point Objective) per service level agreement. Document failover procedures and roles. Test failover procedures quarterly with full team participation. Monitor geo-replication lag and alert if lag exceeds SLA. Maintain separate credentials for failover region. Ensure external audit of disaster recovery controls annually.

### People Analytics Use Cases
- Regional outage in US East region: automatic ZRS failover within same region (1-2 minutes). If both East zones unavailable, manual failover to US Central capacity (4 hours RTO) ensures payroll analytics continue.
- Compliance requirement for Canadian employee data to remain in Canada: Canadian Fabric Capacity with geo-replication to alternate Canadian region, ensuring data never leaves Canada even during failover.
- Financial services regulatory requirement for near-zero RPO: async geo-replication has 30-minute lag, so daily snapshot export to alternate region ensures RPO <24 hours.

### Related Patterns
- **Compatible with:** medallion-architecture, encryption-at-rest-cmk, audit-siem-integration
- **Prerequisites:** None
- **Incompatible with:** None

---

## Cross-Border Data Residency Isolation
**Complexity:** High | **Maturity:** GA
**Fabric Components:** Fabric Capacity, OneLake, Workspace Assignment, Multi-Geo Configuration

### What It Is
Cross-border data residency ensures that employee personal data is stored and processed only within specified geographies per regulatory requirements. For multinational HR analytics, Canadian employees' data (salary, SSN, benefits) must remain in Canada due to PIPEDA. US data must remain in US due to state regulations and employer obligations. Fabric multi-geo capacity configuration assigns workspaces to specific regions; OneLake data is geo-pinned to that region. Cross-border reporting uses aggregate-only views (k-anonymity approach) ensuring individual records cannot be queried across borders. Data sharing uses Shortcuts with filtering, preventing cross-border record-level export. Periodic reviews ensure no data has migrated across borders. Audit logs track cross-border access attempts.

### Pros
- Meets regulatory data residency requirements (PIPEDA, GDPR, local laws) preventing costly compliance violations.
- Enables multi-country operations with confidence that data stays in authorized regions.
- Provides operational resilience: country-level outage affects only that region's operations, not global.

### Cons
- Multi-region capacities increase costs ~2-3x vs. single-region (separate capacity per region).
- Analytics across regions requires federated queries or cross-border aggregates; complex joins are impossible.
- Data migration for employee moves (e.g., employee relocates from Canada to US) requires careful handling: old records deletion or transfer.

### Usage Instructions
1. Create separate Fabric Capacity per geography: Canadian Capacity (Canada Central region), US Capacity (US East 2 region). 2. Create separate workspaces per geography: 'HR-Analytics-CA' in Canadian capacity, 'HR-Analytics-US' in US capacity. 3. Ingest employee data to geo-pinned Lakehouse: Canadian employee table in Canada workspace, US employee table in US workspace. 4. For cross-border reporting, create aggregate-only views: SELECT department, YEAR(dob) as year_of_birth, COUNT(*) as employee_count FROM employees WHERE country='CA' GROUP BY department, YEAR(dob) HAVING COUNT(*) >= 5. 5. Create federated semantic models: Power BI connects to Canadian and US aggregate views, combines aggregates (no record-level data). 6. Prevent cross-border shortcuts: Workspace Sharing > restrict shortcuts to same-region workspaces. 7. Audit cross-border access: Log Analytics tracks queries across regions, alert on suspicious activity. 8. Data migration procedure: terminating employee, update country field, archive to historical table in original region, do not migrate raw records.

### Governance Considerations
> Establish data residency governance committee with legal, compliance, and HR stakeholders per country. Document residency requirements by jurisdiction (PIPEDA, GDPR, state laws). Implement technical enforcement: prevent shortcuts crossing regions, audit logs for attempted cross-border access. Quarterly audit: verify no employee data exists in wrong region. Data transfer agreements: document how employee relocations are handled. Secure deletion: ensure migrated data is permanently deleted from source region.

### People Analytics Use Cases
- Canadian bank with Canadian HQ + US subsidiary: employees are separated by capacity/workspace. Canadian headquarters views all Canadian employee analytics in Canadian workspace (compliant with PIPEDA). US subsidiary views US employee analytics in US workspace. Joint reporting uses aggregates: total Canadian headcount + total US headcount, no cross-border record-level joins.
- Multinational tech company with employees in Canada, US, and EU: separate capacities for each region. Annual global report aggregates at country-group level: 'Canada 5000 employees, US 10000 employees, EU 3000 employees' without exposing individual records.
- Employee relocation: Canadian employee transfers to US. Old record in Canadian Lakehouse is soft-deleted (marked inactive), no migration to US workspace. US onboarding creates new record in US workspace for same employee.

### Related Patterns
- **Compatible with:** medallion-architecture, encryption-at-rest-cmk, disaster-recovery-geo
- **Prerequisites:** None
- **Incompatible with:** None

---

## Disaster Recovery and Geo-Redundancy
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** OneLake, Fabric Capacity, Azure Region Pairs, Zone-Redundant Storage

### What It Is
Disaster recovery ensures business continuity when regional outages occur. OneLake Zone-Redundant Storage (ZRS) replicates data across three availability zones within a region, protecting against zone-level failures. Geo-replication asynchronously copies data to a paired region (e.g., US East 2 to US Central 1), protecting against regional disasters. Fabric Capacity can be provisioned in multiple regions to enable manual failover. For HR analytics, disaster recovery ensures employee data is always available and compliant with data residency laws (e.g., Canadian data stays in Canada region). Multi-geo capacity configuration enables capacity to be deployed in specific regions. Backup procedures include daily snapshots exported to secure storage. Manual failover involves updating connection strings and repointing workspaces to failover capacity in alternate region. Recovery Time Objective (RTO) for manual failover is 4-8 hours; automated failover via service mesh future capability targets RTO <15 minutes.

### Pros
- ZRS provides automatic replication without application changes, protecting against zone and data center failures with no additional cost.
- Geo-replication enables regional compliance (e.g., Canadian data in Canada) and disaster recovery to another region, meeting business continuity SLAs.
- Manual failover procedures are tested and documented, enabling rapid recovery with minimal training.

### Cons
- Geo-replication introduces asynchronous delay (minutes to hours); recent data changes may not be replicated if failover occurs immediately after write.
- Manual failover requires human action and coordination, typically taking 4-8 hours; automated failover is not yet available.
- Multi-region Fabric Capacity costs increase significantly; maintaining hot-hot failover doubles capacity costs vs. cold standby.

### Usage Instructions
1. Enable ZRS on OneLake workspace: Workspace Settings > Storage Redundancy > Zone-Redundant Storage. 2. Configure geo-replication: Workspace Settings > Disaster Recovery > Enable Geo-Replication to paired region (e.g., East 2 to Central 1). 3. Create Data Factory pipeline for daily snapshot export: copy all Lakehouse tables to Azure Storage Account in alternate region. 4. Document failover runbook: 1) Declare disaster, 2) Notify stakeholders, 3) Verify failover region readiness, 4) Update Fabric workspace connection to failover capacity, 5) Repoint Power BI datasets to failover semantic models, 6) Validate data integrity in failover region. 5. Conduct quarterly disaster recovery drill: simulate regional failure, execute failover, validate analytics in alternate region, measure RTO. 6. Maintain failover capacity in standby mode or scale down when not in use.

### Governance Considerations
> Establish disaster recovery committee with IT, business continuity, and HR stakeholders. Define RTO (Recovery Time Objective) and RPO (Recovery Point Objective) per service level agreement. Document failover procedures and roles. Test failover procedures quarterly with full team participation. Monitor geo-replication lag and alert if lag exceeds SLA. Maintain separate credentials for failover region. Ensure external audit of disaster recovery controls annually.

### People Analytics Use Cases
- Regional outage in US East region: automatic ZRS failover within same region (1-2 minutes). If both East zones unavailable, manual failover to US Central capacity (4 hours RTO) ensures payroll analytics continue.
- Compliance requirement for Canadian employee data to remain in Canada: Canadian Fabric Capacity with geo-replication to alternate Canadian region, ensuring data never leaves Canada even during failover.
- Financial services regulatory requirement for near-zero RPO: async geo-replication has 30-minute lag, so daily snapshot export to alternate region ensures RPO <24 hours.

### Related Patterns
- **Compatible with:** medallion-architecture, encryption-at-rest-cmk, audit-siem-integration
- **Prerequisites:** None
- **Incompatible with:** None

---

## Cross-Border Data Residency Isolation
**Complexity:** High | **Maturity:** GA
**Fabric Components:** Fabric Capacity, OneLake, Workspace Assignment, Multi-Geo Configuration

### What It Is
Cross-border data residency ensures that employee personal data is stored and processed only within specified geographies per regulatory requirements. For multinational HR analytics, Canadian employees' data (salary, SSN, benefits) must remain in Canada due to PIPEDA. US data must remain in US due to state regulations and employer obligations. Fabric multi-geo capacity configuration assigns workspaces to specific regions; OneLake data is geo-pinned to that region. Cross-border reporting uses aggregate-only views (k-anonymity approach) ensuring individual records cannot be queried across borders. Data sharing uses Shortcuts with filtering, preventing cross-border record-level export. Periodic reviews ensure no data has migrated across borders. Audit logs track cross-border access attempts.

### Pros
- Meets regulatory data residency requirements (PIPEDA, GDPR, local laws) preventing costly compliance violations.
- Enables multi-country operations with confidence that data stays in authorized regions.
- Provides operational resilience: country-level outage affects only that region's operations, not global.

### Cons
- Multi-region capacities increase costs ~2-3x vs. single-region (separate capacity per region).
- Analytics across regions requires federated queries or cross-border aggregates; complex joins are impossible.
- Data migration for employee moves (e.g., employee relocates from Canada to US) requires careful handling: old records deletion or transfer.

### Usage Instructions
1. Create separate Fabric Capacity per geography: Canadian Capacity (Canada Central region), US Capacity (US East 2 region). 2. Create separate workspaces per geography: 'HR-Analytics-CA' in Canadian capacity, 'HR-Analytics-US' in US capacity. 3. Ingest employee data to geo-pinned Lakehouse: Canadian employee table in Canada workspace, US employee table in US workspace. 4. For cross-border reporting, create aggregate-only views: SELECT department, YEAR(dob) as year_of_birth, COUNT(*) as employee_count FROM employees WHERE country='CA' GROUP BY department, YEAR(dob) HAVING COUNT(*) >= 5. 5. Create federated semantic models: Power BI connects to Canadian and US aggregate views, combines aggregates (no record-level data). 6. Prevent cross-border shortcuts: Workspace Sharing > restrict shortcuts to same-region workspaces. 7. Audit cross-border access: Log Analytics tracks queries across regions, alert on suspicious activity. 8. Data migration procedure: terminating employee, update country field, archive to historical table in original region, do not migrate raw records.

### Governance Considerations
> Establish data residency governance committee with legal, compliance, and HR stakeholders per country. Document residency requirements by jurisdiction (PIPEDA, GDPR, state laws). Implement technical enforcement: prevent shortcuts crossing regions, audit logs for attempted cross-border access. Quarterly audit: verify no employee data exists in wrong region. Data transfer agreements: document how employee relocations are handled. Secure deletion: ensure migrated data is permanently deleted from source region.

### People Analytics Use Cases
- Canadian bank with Canadian HQ + US subsidiary: employees are separated by capacity/workspace. Canadian headquarters views all Canadian employee analytics in Canadian workspace (compliant with PIPEDA). US subsidiary views US employee analytics in US workspace. Joint reporting uses aggregates: total Canadian headcount + total US headcount, no cross-border record-level joins.
- Multinational tech company with employees in Canada, US, and EU: separate capacities for each region. Annual global report aggregates at country-group level: 'Canada 5000 employees, US 10000 employees, EU 3000 employees' without exposing individual records.
- Employee relocation: Canadian employee transfers to US. Old record in Canadian Lakehouse is soft-deleted (marked inactive), no migration to US workspace. US onboarding creates new record in US workspace for same employee.

### Related Patterns
- **Compatible with:** medallion-architecture, encryption-at-rest-cmk, disaster-recovery-geo
- **Prerequisites:** None
- **Incompatible with:** None

---

