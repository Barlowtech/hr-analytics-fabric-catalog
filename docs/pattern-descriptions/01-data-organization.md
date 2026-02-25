# Data Organization and Structuring

Data organization forms the foundation of any effective analytics platform. In the context of HR analytics,
how you structure and organize employee data, organizational hierarchies, and historical records directly impacts
the speed and accuracy of insights your teams can generate.

This domain covers patterns for implementing lakehouse architectures, designing efficient data models, and establishing
clear data quality boundaries. By following these patterns, you create a scalable, maintainable foundation that supports
everything from basic HR reporting to advanced predictive analytics.

The patterns in this section address the critical challenge of moving data from raw sources through progressively refined
layers, ensuring that data quality improves at each stage while maintaining an audit trail and supporting rapid queries.

---

## Medallion Architecture (Bronze-Silver-Gold)
**Complexity:** High | **Maturity:** GA
**Fabric Components:** Lakehouse, OneLake, Spark Notebooks, Delta Lake

### What It Is
The medallion architecture separates raw data ingestion, cleansed data, and business-ready analytics data into distinct layers. For HR analytics, employee data moves through Bronze (raw), Silver (standardized), and Gold (business-ready) layers.

### Pros
- Provides clear separation of concerns with distinct data quality boundaries.
- Enables independent scaling and optimization of each layer.
- Facilitates governance by creating controlled access points.

### Cons
- Introduces operational complexity with three layers.
- Can increase storage costs if not properly optimized.
- Requires upfront investment in data modeling.

### Usage Instructions
1. Create three folders: Bronze, Silver, Gold. 2. Land raw data into Bronze. 3. Build transformations in Silver. 4. Create final tables in Gold. 5. Apply labels progressively. 6. Establish refresh schedules.

### Governance Considerations
> Implement RLS at Gold layer and restrict Bronze/Silver access to engineers. Apply sensitivity labels to personal data. Maintain transformation logs for audits.

### People Analytics Use Cases
- Employee master repository moving through all layers.
- Payroll analytics data mart with restricted raw salary details.
- Organizational analytics foundation with normalized hierarchies.

### Related Patterns
- **Compatible with:** delta-lake-partitioning, onelake-shortcuts, spark-notebook-etl, dataflow-gen2
- **Prerequisites:** None
- **Incompatible with:** None

---

## Delta Lake Partitioning Strategy
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Lakehouse, Delta Lake, Spark Notebooks

### What It Is
Partitioning divides large tables into segments based on column values like date or department, enabling Spark to skip irrelevant partitions during queries.

### Pros
- Reduces query execution time through predicate pushdown.
- Reduces compute and storage costs by avoiding full scans.
- Simplifies data lifecycle management for old partitions.

### Cons
- Poorly chosen columns degrade performance.
- Over-partitioning requires frequent compaction.
- Adds complexity to pipeline logic.

### Usage Instructions
1. Analyze query patterns. 2. Select 1-3 partition columns. 3. Create table with PARTITIONED BY. 4. Ingest data with partition columns. 5. Run ANALYZE TABLE COMPUTE STATISTICS. 6. Monitor and optimize quarterly.

### Governance Considerations
> Align partition columns with RLS policies. Document strategy in data catalog. Monitor partition drift. Ensure archived partitions follow retention policies.

### People Analytics Use Cases
- Payroll trend analysis across decade with fast access to recent periods.
- Attendance pattern retrieval without scanning all records.
- Time-travel org hierarchy analysis.

### Related Patterns
- **Compatible with:** medallion-architecture, lakehouse-warehouse-selection, spark-notebook-etl
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

## Lakehouse vs Warehouse Selection
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Lakehouse, Warehouse, OneLake, Spark Notebooks

### What It Is
Lakehouse works well for unstructured data and ML; Warehouse for structured relational analytics. Many use both in parallel.

### Pros
- Optimal tool selection for different workloads.
- Lakehouse provides flexibility; Warehouse ensures consistency.
- Supports incremental adoption and migration.

### Cons
- Operating both increases operational overhead.
- Performance strategies differ significantly.
- Teams must understand distinct capabilities.

### Usage Instructions
1. Assess workload type. 2. Structured HR reporting → Warehouse. 3. Exploratory analysis → Lakehouse. 4. Semi-structured → Lakehouse. 5. If both needed: Lakehouse Bronze/Silver, Warehouse for reporting. 6. Use shortcuts.

### Governance Considerations
> Warehouse provides stricter governance through schema enforcement. Restrict Warehouse to certified analytics. Use Lakehouse for non-sensitive exploration.

### People Analytics Use Cases
- Operational HR dashboards in Warehouse.
- Survey analysis and churn modeling in Lakehouse.
- ML pipelines in Lakehouse, results in Warehouse.

### Related Patterns
- **Compatible with:** medallion-architecture, direct-lake-semantic-model
- **Prerequisites:** None
- **Incompatible with:** None

---

## OneLake Shortcuts for Data Sharing
**Complexity:** Low | **Maturity:** GA
**Fabric Components:** OneLake, Lakehouse, Warehouse, Shortcuts

### What It Is
Shortcuts point to data in other Lakehouses, Warehouses, or external storage. Finance maintains employee master; HR and Recruiting create shortcuts to it.

### Pros
- Eliminates duplication and maintains single source of truth.
- Zero-copy reduces costs; updates visible immediately.
- Simplifies cross-team collaboration.

### Cons
- Cross-workspace latency can degrade performance.
- Shortcuts obscure ownership and governance.
- Lineage becomes harder to debug.

### Usage Instructions
1. Identify source of truth tables. 2. Create Lakehouse in consumer team. 3. Right-click folder > New shortcut. 4. Select source table. 5. Query like normal tables. 6. Monitor performance.

### Governance Considerations
> Shortcuts must point to governed tables. Establish data contracts for schema stability. Document in data catalog. Apply workspace permissions. Use for read-only reference data.

### People Analytics Use Cases
- Finance employee master accessed via shortcuts by HR and Recruiting.
- Shared org hierarchy referenced across teams.
- Reducing storage by shortcutting payroll data.

### Related Patterns
- **Compatible with:** medallion-architecture, lakehouse-warehouse-selection
- **Prerequisites:** None
- **Incompatible with:** None

---

## Direct Lake Semantic Model
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Semantic Model, Power BI, OneLake, Delta Lake, Lakehouse

### What It Is
Direct Lake bypasses VertiPaq import, providing freshness of DirectQuery with import speed. Gold-layer tables feed Power BI without duplication.

### Pros
- Real-time data access without import overhead.
- Eliminates storage duplication.
- Combines import performance with DirectQuery freshness.

### Cons
- Requires well-optimized Delta tables.
- Not all Power BI transformations supported.
- Optimization less transparent than import mode.

### Usage Instructions
1. Ensure Gold tables are optimized. 2. Create semantic model. 3. Select Direct Lake mode. 4. Browse and select Gold tables. 5. Create relationships. 6. Build reports. 7. Monitor performance.

### Governance Considerations
> Direct Lake exposes lakehouse structure; govern before creating models. Control who modifies underlying tables. Apply sensitivity labels. Document contracts. Prevent accidental deletions.

### People Analytics Use Cases
- Real-time HR dashboards from Gold tables.
- Live payroll cost dashboards.
- Quick BI iteration using Direct Lake.

### Related Patterns
- **Compatible with:** medallion-architecture, lakehouse-warehouse-selection, delta-lake-partitioning
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

## Hub-and-Spoke Workspace Design
**Complexity:** Medium | **Maturity:** GA
**Fabric Components:** Workspaces, OneLake, Lakehouse, Shortcuts

### What It Is
Central Hub maintains employee master, org structure, cost centers. Spokes use shortcuts to reference Hub and build domain analytics.

### Pros
- Centralizes reference data governance.
- Enables autonomous spoke teams.
- Simplifies permission management.

### Cons
- Cross-workspace dependencies add complexity.
- Hub requires dedicated team.
- Network latency for shortcuts.

### Usage Instructions
1. Create Hub workspace. 2. Populate with reference tables. 3. Create Spoke workspaces. 4. Spoke teams create shortcuts to Hub. 5. Spoke builds own layers. 6. Establish data review board. 7. Document dependencies.

### Governance Considerations
> Hub requires clear ownership and change management. Strict Hub permissions: stewards only. Enforce RLS at Spoke level. Document contracts. Monitor dependencies.

### People Analytics Use Cases
- Central HR Hub with Recruiting, Compensation spokes.
- Finance Hub with HR spoke for cost allocation.
- Executive Hub with HR spoke for talent alignment.

### Related Patterns
- **Compatible with:** medallion-architecture, onelake-shortcuts
- **Prerequisites:** medallion-architecture
- **Incompatible with:** None

---

