# Business Intelligence and Reporting

Business intelligence transforms processed HR data into interactive dashboards, self-service reports, and
executive-level insights. This domain covers patterns for building performant BI solutions that enable stakeholders
across HR, finance, operations, and leadership to explore data and find answers.

The patterns in this section focus on creating responsive, interactive experiences that support various analytical needs:
from operational dashboards for HR teams to strategic workforce planning tools for executives, to self-service analytics
for individual contributors.

Effective BI patterns ensure that insights reach the right stakeholders in formats they can act on, driving better decisions
throughout the organization.

---

## Direct Lake Power BI Semantic Models
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Power BI, Semantic Model, Direct Lake, Lakehouse

### What It Is
Gold tables feed Power BI directly via Direct Lake. No nightly imports. BI analysts refresh tables instantly. Dashboards always show latest data.

### Pros
- Real-time data for dashboards.
- No import bottleneck.
- Simplified data pipeline.

### Cons
- Requires optimized Gold tables.
- Less transformation flexibility.
- Network latency possible.

### Usage Instructions
1. Create semantic model in Workspace. 2. Connect to Gold tables via Direct Lake. 3. Define relationships. 4. Create measures. 5. Build reports. 6. Publish. 7. Monitor performance.

### Governance Considerations
> Gold tables must be governed. Control who modifies lakehouse. Apply RLS at semantic model level. Document data contracts.

### People Analytics Use Cases
- Real-time HR dashboard from Gold tables.
- Executive payroll dashboard.
- Live recruiting pipeline dashboard.

### Related Patterns
- **Compatible with:** medallion-architecture, direct-lake-semantic-model, delta-lake-partitioning
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

## Storage Mode Selection (Import/DirectQuery/Dual)
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Power BI, Semantic Model, Warehouse, Lakehouse

### What It Is
Import small lookup tables for speed. DirectQuery large slow-changing fact tables. Dual mode combines both for flexibility.

### Pros
- Optimizes performance and refresh time.
- Reduces Premium capacity utilization.
- Flexibility for heterogeneous requirements.

### Cons
- Increases modeling complexity.
- DirectQuery can be slow without optimization.
- Users must understand modes.

### Usage Instructions
1. Analyze table size and query frequency. 2. Small/frequently accessed = Import. 3. Large/slow-changing = DirectQuery. 4. Mixed = Dual. 5. Monitor refresh times. 6. Adjust modes based on perf.

### Governance Considerations
> Document storage mode decisions. Monitor refresh failures. Update source query optimization. Test DirectQuery performance.

### People Analytics Use Cases
- Import employee dimension; DirectQuery large payroll facts.
- Dual mode org hierarchy with frequent ref lookup.
- Import cost center lookup; DirectQuery salary facts.

### Related Patterns
- **Compatible with:** directlake-power-bi, certified-semantic-model
- **Prerequisites:** None
- **Incompatible with:** None

---

## Composite Models (Multi-Source Mashing)
**Complexity:** High | **Maturity:** GA
**Fabric Components:** Power BI, Semantic Model, Composite Model, Multiple Sources

### What It Is
Employee master from Lakehouse, payroll from Warehouse, survey data from Excel. Composite model joins across sources.

### Pros
- Unified analytics across sources.
- Reduces data movement.
- Flexible source management.

### Cons
- Query complexity increases.
- Cross-source joins can be slow.
- Debugging difficult.

### Usage Instructions
1. Create semantic model. 2. Add tables from multiple sources. 3. Define relationships across sources. 4. Create measures. 5. Test query performance. 6. Monitor.

### Governance Considerations
> Document source integration logic. Monitor cross-source join performance. Establish data ownership across sources.

### People Analytics Use Cases
- Employee Lakehouse table joined with payroll Warehouse table.
- Org Lakehouse joined with survey results from Excel.
- Performance Lakehouse joined with compensation Warehouse.

### Related Patterns
- **Compatible with:** storage-mode-selection, certified-semantic-model
- **Prerequisites:** None
- **Incompatible with:** None

---

## Certified Semantic Models
**Complexity:** Low | **Maturity:** GA
**Fabric Components:** Power BI, Semantic Model, Workspace

### What It Is
Gold-layer semantic models certified by BI team mark metrics as authoritative. Analysts use certified models for consistency.

### Pros
- Ensures metric consistency across dashboards.
- Reduces metric duplication.
- Facilitates self-service BI.

### Cons
- Requires strong BI governance.
- Slows new model deployment.
- Can bottleneck innovation.

### Usage Instructions
1. Build semantic model. 2. Document metrics and definitions. 3. Have BI team certify. 4. Mark as Certified. 5. Analysts build reports. 6. Update as needed.

### Governance Considerations
> Establish certification criteria. Document metric definitions. Review before certification. Update certification on changes.

### People Analytics Use Cases
- Certified headcount metric used across dashboards.
- Certified FTE calculation model.
- Certified cost per hire metric.

### Related Patterns
- **Compatible with:** directlake-power-bi, storage-mode-selection, composite-model
- **Prerequisites:** None
- **Incompatible with:** None

---

## Paginated Reports for Formal Documents
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Power BI, Paginated Reports, Warehouse, Semantic Model

### What It Is
Paginated reports in Power BI for formatted output. Employee tax statements, OFCCP compliance reports, board summaries.

### Pros
- Pixel-perfect formatting for formal documents.
- Supports complex layouts and headers.
- Suitable for printing and distribution.

### Cons
- Slower to develop than dashboards.
- Limited interactivity.
- Requires RDL knowledge.

### Usage Instructions
1. Create paginated report in Power BI. 2. Define parameters. 3. Design layout. 4. Connect to data source. 5. Format for printing. 6. Test output. 7. Schedule.

### Governance Considerations
> Formal reports require approval. Document generation logic. Maintain version history. Ensure data accuracy.

### People Analytics Use Cases
- Employee tax statements generated monthly.
- OFCCP compliance report certification.
- Board summary with specific formatting.
- Payroll audit report.

### Related Patterns
- **Compatible with:** storage-mode-selection, certified-semantic-model
- **Prerequisites:** None
- **Incompatible with:** None

---

## Power BI Metrics Scorecards
**Complexity:** Low | **Maturity:** GA
**Fabric Components:** Power BI, Metrics, Semantic Model

### What It Is
Headcount goal vs actual, cost per hire vs target, time-to-fill trend. Scorecard shows metric, trend, variance from goal.

### Pros
- Executive-friendly visualization.
- Quick identification of variances.
- Supports scorecards at any granularity.

### Cons
- Requires careful metric selection.
- Not suited for deep analysis.
- Goal management overhead.

### Usage Instructions
1. Select metrics. 2. Define goals. 3. Create scorecard visual. 4. Connect to semantic model. 5. Format for execs. 6. Publish.

### Governance Considerations
> Goals reviewed and approved. Metric definitions consistent. Regular updates. Executive alignment on priorities.

### People Analytics Use Cases
- Executive dashboard with headcount, cost, turnover metrics.
- Department scorecard with regional goals.
- Recruiting metrics scorecard with time-to-fill, cost-per-hire.

### Related Patterns
- **Compatible with:** certified-semantic-model, directlake-power-bi
- **Prerequisites:** None
- **Incompatible with:** None

---

## Power BI Deployment Pipelines
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Power BI, Deployment Pipelines, Semantic Model, Reports

### What It Is
Dev → Stage → Prod. Semantic models and reports tested in stage before prod deployment. Reduces errors in production.

### Pros
- Reduces deployment errors.
- Enables testing before production.
- Audit trail of changes.

### Cons
- Setup complexity.
- Requires discipline in dev/stage separation.
- Can slow development cycles.

### Usage Instructions
1. Create three workspaces: Dev, Stage, Prod. 2. Set up pipeline. 3. Develop in Dev. 4. Deploy to Stage. 5. Test. 6. Deploy to Prod. 7. Monitor.

### Governance Considerations
> Change approval for Prod. Test in Stage. Monitor Prod performance. Rollback procedures. Post-mortem on failures.

### People Analytics Use Cases
- Develop dashboard in Dev; promote through Stage to Prod.
- Semantic model change testing before production.
- New report rollout with staging validation.

### Related Patterns
- **Compatible with:** certified-semantic-model, directlake-power-bi
- **Prerequisites:** None
- **Incompatible with:** None

---

