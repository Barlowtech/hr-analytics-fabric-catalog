# HR Analytics Fabric Catalog

**A comprehensive guide to implementing people analytics on Microsoft Fabric**

## What This Is

The HR Analytics Fabric Catalog is a collection of tested patterns, best practices, and implementation guidance for building
comprehensive people analytics solutions using Microsoft Fabric. This catalog brings together patterns for data organization,
transformation, governance, business intelligence, machine learning, and more—specifically tailored for HR analytics use cases.

Whether you're building your first HR analytics solution or modernizing an existing one, this catalog provides:

- **8 Domain Areas:** Comprehensive coverage from data organization through data sharing
- **73 Patterns:** Tested approaches with complexity assessments, governance considerations, and use cases
- **Implementation Guidance:** Practical instructions, code examples, and best practices
- **Governance Focus:** Special attention to the unique security and compliance requirements of HR data

This catalog reflects real-world implementations and lessons learned from organizations building analytics platforms
on Microsoft Fabric. It's designed to help you move faster while avoiding common pitfalls.

## Quick Start

### Using the Pattern Builder HTML App
1. Open `pattern-builder.html` in your web browser
2. Browse patterns by domain, search by name, and explore relationships
3. Filter by complexity, maturity, and other attributes
4. Export pattern summaries for team discussions

### Using the Streamlit Application
```bash
cd streamlit
streamlit run app.py
```

The Streamlit app provides:
- Interactive pattern explorer
- Domain-specific views
- Pattern relationships and dependencies
- Implementation checklist generation

## Pattern Catalog

| Pattern | Domain | Complexity | Maturity |
|---------|--------|------------|----------|
| Medallion Architecture (Bronze-Silver-Gold) | Data Organization and Structuring | High | GA |
| Delta Lake Partitioning Strategy | Data Organization and Structuring | Medium | GA |
| Lakehouse vs Warehouse Selection | Data Organization and Structuring | Medium | GA |
| OneLake Shortcuts for Data Sharing | Data Organization and Structuring | Low | GA |
| Direct Lake Semantic Model | Data Organization and Structuring | Medium | GA |
| Hub-and-Spoke Workspace Design | Data Organization and Structuring | Medium | GA |
| Spark Notebook ETL Pipelines | Data Transformation and Processing | High | GA |
| Dataflow Gen2 Low-Code Transformations | Data Transformation and Processing | Low | GA |
| Incremental Loading with Watermarks | Data Transformation and Processing | Medium | GA |
| Slowly Changing Dimensions Type 2 | Data Transformation and Processing | Medium | GA |
| Change Data Capture (CDC) for Auditing | Data Transformation and Processing | Medium | GA |
| dbt Integration for Data Transformation | Data Transformation and Processing | Medium | GA |
| Data Quality Validation Framework | Data Transformation and Processing | Medium | GA |
| Microsoft Purview Data Map | Data Governance and Security | Medium | GA |
| Sensitivity Labels for Data Classification | Data Governance and Security | Medium | GA |
| Row-Level Security (RLS) at Gold Layer | Data Governance and Security | Medium | GA |
| Dynamic Data Masking for Development/Test | Data Governance and Security | Medium | GA |
| Attribute-Based Access Control (ABAC) | Data Governance and Security | High | GA |
| Workspace Permission Governance | Data Governance and Security | Low | GA |
| Direct Lake Power BI Semantic Models | Business Intelligence and Reporting | Medium | GA |
| Storage Mode Selection (Import/DirectQuery/Dual) | Business Intelligence and Reporting | Medium | GA |
| Composite Models (Multi-Source Mashing) | Business Intelligence and Reporting | High | GA |
| Certified Semantic Models | Business Intelligence and Reporting | Low | GA |
| Paginated Reports for Formal Documents | Business Intelligence and Reporting | Medium | GA |
| Power BI Metrics Scorecards | Business Intelligence and Reporting | Low | GA |
| Power BI Deployment Pipelines | Business Intelligence and Reporting | Medium | GA |
| Batch Inference Pipelines | Machine Learning and Traditional AI | High | GA |
| Feature Store Implementation | Machine Learning and Traditional AI | Medium | GA |
| MLflow Model Registry | Machine Learning and Traditional AI | Medium | GA |
| Model Drift Detection and Monitoring | Machine Learning and Traditional AI | High | Preview |
| Fairness and Bias Evaluation | Machine Learning and Traditional AI | High | Emerging |
| Champion-Challenger Model Testing | Machine Learning and Traditional AI | High | GA |
| RAG (Retrieval-Augmented Generation) Fabric-Grounded | Generative AI and Conversational Interfaces | High | Preview |
| Secure Conversational Interface with RLS | Generative AI and Conversational Interfaces | High | Preview |
| Azure AI Foundry Integration | Generative AI and Conversational Interfaces | Medium | GA |
| Copilot Studio with Fabric Data Grounding | Generative AI and Conversational Interfaces | Medium | GA |
| Semantic Search with Vector Embeddings | Generative AI and Conversational Interfaces | High | Preview |
| LLM Auto-Generated Narratives | Generative AI and Conversational Interfaces | Medium | Preview |
| HR-Specific AI Guardrails and Safety | Generative AI and Conversational Interfaces | High | Emerging |
| Data Activator (Reflex) for Auto-Actions | Alerting, Automation, and Operational Intelligence | Medium | GA |
| Power Automate Workflows with Data Triggers | Alerting, Automation, and Operational Intelligence | Low | GA |
| Metric Summarization Engine | Alerting, Automation, and Operational Intelligence | Low | GA |
| SLA Freshness Monitoring | Alerting, Automation, and Operational Intelligence | Low | GA |
| Automated Escalation and Routing | Alerting, Automation, and Operational Intelligence | Medium | GA |
| Cross-Workspace Data Sharing via Shortcuts | Data Sharing and Distribution | Low | GA |
| Cross-Tenant Data Sharing (B2B Scenarios) | Data Sharing and Distribution | High | Preview |
| Semantic Model Certification Pipeline | Data Sharing and Distribution | Medium | GA |
| REST API Exposure and Management | Data Sharing and Distribution | Medium | GA |
| Dataset Subscription and Change Alerts | Data Sharing and Distribution | Medium | Preview |
| Encryption at Rest with Customer-Managed Keys | Data Governance and Security | Medium | GA |
| Data Loss Prevention Policy Enforcement | Data Governance and Security | Medium | GA |
| PII Tokenization and Pseudonymization | Data Transformation and Processing | High | Emerging |
| Automated Data Retention and Purge Pipeline | Data Transformation and Processing | High | Emerging |
| Statistical Anonymization for HR Analytics | Data Governance and Security | High | Emerging |
| Audit Log Export and SIEM Integration | Data Governance and Security | Medium | GA |
| Data Subject Request Fulfillment Pipeline | Data Governance and Security | High | Emerging |
| Disaster Recovery and Geo-Redundancy | Data Sharing and Distribution | Medium | GA |
| Network Isolation with Private Endpoints | Data Governance and Security | High | GA |
| Just-in-Time Privileged Access Management | Data Governance and Security | Medium | GA |
| Dual-Approval Change Management Pipeline | Data Transformation and Processing | Medium | Emerging |
| Cross-Border Data Residency Isolation | Data Sharing and Distribution | High | GA |
| Encryption at Rest with Customer-Managed Keys | Data Governance and Security | Medium | GA |
| Data Loss Prevention Policy Enforcement | Data Governance and Security | Medium | GA |
| PII Tokenization and Pseudonymization | Data Transformation and Processing | High | Emerging |
| Automated Data Retention and Purge Pipeline | Data Transformation and Processing | High | Emerging |
| Statistical Anonymization for HR Analytics | Data Governance and Security | High | Emerging |
| Audit Log Export and SIEM Integration | Data Governance and Security | Medium | GA |
| Data Subject Request Fulfillment Pipeline | Data Governance and Security | High | Emerging |
| Disaster Recovery and Geo-Redundancy | Data Sharing and Distribution | Medium | GA |
| Network Isolation with Private Endpoints | Data Governance and Security | High | GA |
| Just-in-Time Privileged Access Management | Data Governance and Security | Medium | GA |
| Dual-Approval Change Management Pipeline | Data Transformation and Processing | Medium | Emerging |
| Cross-Border Data Residency Isolation | Data Sharing and Distribution | High | GA |

## Repository Structure

```
hr-analytics-fabric-catalog/
├── README.md                          # This file
├── patterns.json                      # Complete pattern definitions (machine-readable)
├── pattern-builder.html               # Interactive web-based pattern explorer
├── research-notes.md                  # Summary of patterns by domain
├── .gitignore                         # Git ignore rules
│
├── docs/
│   ├── pattern-descriptions/          # Domain-specific pattern guides
│   │   ├── 01-data-organization.md
│   │   ├── 02-transformation-processing.md
│   │   ├── 03-governance-security.md
│   │   ├── 04-business-intelligence.md
│   │   ├── 05-machine-learning.md
│   │   ├── 06-generative-ai.md
│   │   ├── 07-alerting-automation.md
│   │   └── 08-data-sharing.md
│   ├── governance-guide/              # Governance and compliance documentation
│   ├── fabric-reference/              # Fabric component reference
│   └── usage-guide/                   # Implementation guidance
│
├── streamlit/                         # Streamlit application
│   ├── app.py
│   └── requirements.txt
│
└── .git/                              # Version control
```

## Document Library

| Document | Subject | Type |
|----------|---------|------|
| 01-data-organization.md | Data Organization and Structuring | Domain reference |
| 02-transformation-processing.md | Transformation and Processing | Domain reference |
| 03-governance-security.md | Governance and Security | Domain reference |
| 04-business-intelligence.md | Business Intelligence and Reporting | Domain reference |
| 05-machine-learning.md | Machine Learning and Predictive Analytics | Domain reference |
| 06-generative-ai.md | Generative AI and Advanced Analytics | Domain reference |
| 07-alerting-automation.md | Alerting and Automation | Domain reference |
| 08-data-sharing.md | Data Sharing and Collaboration | Domain reference |

## Contributing

This catalog is a living document. As you implement these patterns:

1. **Share Lessons Learned:** Document what worked, what didn't, and why
2. **Suggest New Patterns:** If you've solved a problem not covered here, contribute it
3. **Update Based on Feedback:** Help improve the patterns based on real-world use

Please submit pull requests with:
- Clear description of the pattern or improvement
- Real-world context and use cases
- Governance and compliance considerations
- Links to relevant documentation

## Governance Notes

### Data Sensitivity
This catalog focuses on patterns for handling sensitive HR and people data. All implementations should:

- Follow your organization's data classification standards
- Implement appropriate role-based access control (RBAC)
- Apply sensitivity labels to personal data
- Maintain audit trails of data access and transformations
- Comply with relevant regulations (GDPR, CCPA, local employment laws)

### Pattern Maturity
Patterns are marked with maturity levels:
- **GA (General Availability):** Fully supported and recommended for production use
- **Preview:** Available but may change; use with caution
- **Experimental:** Research stage; evaluate carefully before production use

### Complexity Assessment
Patterns are assessed for implementation complexity:
- **Low:** Can be implemented in days with basic skills
- **Medium:** Requires expertise; 1-3 weeks typical implementation
- **High:** Requires significant expertise and planning; 3+ weeks typical

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Last Updated:** 2026-02-25 10:14:12

For questions, feedback, or contributions, please open an issue or submit a pull request.
