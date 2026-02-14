# Medicaid Provider Spending — Pipeline Overview

## What It Does

Analyzes ~227M rows of CMS Medicaid provider spending data through 40 automated analysis sections, generating 58+ CSVs and 43+ visualizations.

## Pipeline Architecture

```
medicaid_analysis/
├── main.py                 # CLI orchestrator
├── utils/                  # Config, formatting, I/O, DB (4 modules)
├── eda/                    # Exploratory data analysis (5 modules)
├── stats/                  # Statistical tests & models (6 modules)
├── providers/              # Provider behavior (7 modules)
├── procedures/             # HCPCS code analysis (4 modules)
├── temporal/               # Time-series analysis (5 modules)
├── visualization/          # Deep-dive charts (3 modules)
└── fraud/                  # Fraud detection (8 modules)
```

**Total: 42 Python modules across 8 packages**

## Quick Start

```bash
cd medicaid_analysis

# Full pipeline (all 40 sections)
uv run main.py

# Quick test with sample data
uv run main.py --sample

# Specific sections
uv run main.py --sections 1 5 32

# Skip fraud detection
uv run main.py --skip-fraud
```

## Sections Overview

| Range | Package | Focus |
|---|---|---|
| S01–S05, S12 | `eda/` | Row counts, trends, top entities, cost efficiency |
| S06, S08–S09, S15, S17–S18, S31 | `stats/` | Anomalies, concentration, correlations, power law, Benford's |
| S07, S10, S13, S16, S24, S27, S29 | `providers/` | Billing patterns, diversity, growth, networks, specialization |
| S14, S23, S26, S30 | `procedures/` | HCPCS categories, co-occurrence, size, lifecycle |
| S11, S19, S21–S22, S25 | `temporal/` | Seasonality, intensity, rolling, YoY, velocity |
| S20, S28, S32 | `visualization/` | Distributions, outlier profiles, executive dashboard |
| S33–S40 | `fraud/` | Upcoding, velocity, phantom, clustering, cost outliers, relationships, temporal, composite scoring |

## Fraud Detection

6 independent detection methods + 1 composite scorer:

1. **Upcoding** — Z-score deviation from peer pricing
2. **Velocity** — Sudden billing volume spikes
3. **Phantom** — Impossible claims/beneficiary ratios
4. **Clustering** — K-Means behavioral profiling
5. **Cost Outliers** — Within-HCPCS IQR outliers
6. **Relationships** — Concentrated billing-servicing pairs
7. **Temporal** — Low-entropy / high-CV patterns
8. **Composite** — Multi-signal risk scoring (Clean/Low/Medium/High)

## Dependencies

`pandas`, `numpy`, `matplotlib`, `seaborn`, `duckdb`, `scipy`, `scikit-learn`
