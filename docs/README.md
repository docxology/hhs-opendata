# HHS Open Data — Documentation

## Projects

### [Medicaid Provider Spending Analysis](../medicaid_analysis)

A 40-section modular analysis pipeline for CMS Medicaid provider-level spending data, covering:

- **Exploratory Data Analysis** (S01–S05, S12)
- **Statistical Modeling** (S06, S08–S09, S15, S17–S18, S31)
- **Provider Behavior** (S07, S10, S13, S16, S24, S27, S29)
- **Procedure Analysis** (S14, S23, S26, S30)
- **Temporal Trends** (S11, S19, S21–S22, S25)
- **Advanced Visualization** (S20, S28, S32)
- **Fraud Detection** (S33–S40)

### Detailed Documentation

| Document | Description |
|---|---|
| [Architecture](../medicaid_analysis/docs/architecture.md) | Package design, data flow, dependency graph |
| [Module Reference](../medicaid_analysis/docs/modules.md) | All 40 functions by package |
| [Section Catalog](../medicaid_analysis/docs/sections.md) | Inputs, outputs, dependencies, methods |
| [Fraud Guide](../medicaid_analysis/docs/fraud_guide.md) | 7 detection methods, thresholds, scoring |
| [Data Dictionary](../medicaid_analysis/docs/data_dictionary.md) | Column definitions, dataset statistics |
| [Configuration](../medicaid_analysis/docs/configuration.md) | CLI options, logging, directory structure |
| [Contributing](../medicaid_analysis/docs/contributing.md) | How to add new analysis sections |

## Data Sources

- **CMS Medicaid Provider Spending**: Provider-level utilization and spending data
  - ~227M rows, 617K billing providers, 10.8K HCPCS codes
  - Columns: NPI, HCPCS, month, paid, claims, beneficiaries
