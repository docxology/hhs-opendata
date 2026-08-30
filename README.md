# HHS Open Data — Medicaid Provider Spending

Analysis of the **Medicaid Provider Spending** dataset published by the U.S. Department of Health & Human Services.

> **Source:** <https://opendata.hhs.gov/datasets/medicaid-provider-spending/>

## Dataset

| Column | Type | Description |
|---|---|---|
| `BILLING_PROVIDER_NPI_NUM` | string | National Provider Identifier of the billing provider |
| `SERVICING_PROVIDER_NPI_NUM` | string | National Provider Identifier of the servicing provider |
| `HCPCS_CODE` | string | Healthcare Common Procedure Coding System code |
| `CLAIM_FROM_MONTH` | date | Aggregation month (`YYYY-MM-01`) |
| `TOTAL_UNIQUE_BENEFICIARIES` | integer | Unique beneficiaries for this provider / procedure / month |
| `TOTAL_CLAIMS` | integer | Total claims for this provider / procedure / month |
| `TOTAL_PAID` | float | Total amount paid by Medicaid (USD) |

- **Coverage:** January 2018 – December 2024
- **Granularity:** Provider (NPI) × HCPCS Code × Month
- **Full dataset:** ~227 million rows, ~617K billing NPIs, ~10.9K HCPCS codes, ~11 GB CSV (~3.4 GB compressed)

## Repository Layout

```
hhs-opendata/
├── README.md               ← this file
├── AGENTS.md               ← guidelines for AI agents
├── data/                   ← raw dataset (git-ignored)
│   └── medicaid-provider-spending.csv
├── docs/                   ← documentation hub (README + pipeline overview)
├── manuscript/             ← section stubs for a write-up (all content TODO-OWNER)
└── medicaid_analysis/      ← the analysis pipeline (own pyproject.toml, run with uv)
    ├── main.py             ← CLI orchestrator: all 40 analysis sections
    ├── run_multi_scale.py  ← runs the pipeline at 1/10/50/100% sample scales
    ├── create_sample.py    ← creates Bernoulli sample CSVs from the full dataset
    ├── eda/ stats/ providers/ procedures/ temporal/ visualization/ fraud/
    ├── utils/              ← config, DuckDB helpers, formatting, I/O
    ├── tests/              ← pytest suite (imports, CLI, integration on sample data)
    ├── docs/               ← architecture, modules, sections, fraud guide, data dictionary
    ├── output/             ← generated CSVs (incl. per-scale 1pct/10pct/50pct/100pct + fraud/)
    └── plots/              ← generated PNGs (same per-scale layout)
```

## Quick Start

```bash
# 1. Install dependencies (requires uv)
cd medicaid_analysis
uv sync

# 2. Run the full 40-section analysis on the full dataset
uv run main.py

# Alternatives
uv run main.py --sample          # use data/sample.csv (1% sample) instead
uv run main.py --sections 1 2 5  # specific sections only
uv run main.py --skip-fraud      # skip fraud sections 33-40
uv run main.py --csv <path>      # analyse an arbitrary CSV

# Multi-scale runs → output/{1pct,10pct,50pct,100pct}/ and plots/{1pct,...}/
uv run run_multi_scale.py                 # all four scales (needs the full CSV)
uv run run_multi_scale.py --scales 1 10   # subset; auto-creates missing samples

# Create sample CSVs explicitly
uv run create_sample.py --pct 1 10
```

Output is written to `medicaid_analysis/output/` and `medicaid_analysis/plots/`
(or the per-scale subfolders when run through `run_multi_scale.py`, which sets
`MEDICAID_OUTPUT_DIR` / `MEDICAID_PLOTS_DIR`).

## Analysis Contents

40 sections across 8 subpackages:

1. **Exploratory Data Analysis** (`eda/`, S01–S05, S12) — row counts, monthly/yearly trends, top procedures/providers, cost efficiency, high-value claims
2. **Statistics** (`stats/`, S06, S08–S09, S15, S17–S18, S31) — z-score + Isolation-Forest anomalies, concentration (Gini/HHI), correlations, power law, normality tests, spending deciles, Benford's Law
3. **Providers** (`providers/`, S07, S10, S13, S16, S24, S27, S29) — billing vs servicing, procedure diversity, growth, networks, tenure, specialization, market share
4. **Procedures** (`procedures/`, S14, S23, S26, S30) — HCPCS categories, co-occurrence, claims size, lifecycle
5. **Temporal** (`temporal/`, S11, S19, S21–S22, S25) — seasonality, beneficiary intensity, rolling/cumulative metrics, YoY, spending velocity
6. **Visualization** (`visualization/`, S20, S28, S32) — distribution deep dives, outlier profiles, executive dashboard
7. **Fraud Detection** (`fraud/`, S33–S40) — upcoding, billing-velocity anomalies, phantom billing, clustering, cost outliers, relationship anomalies, temporal anomalies, composite risk score

## Technology

| Tool | Purpose |
|---|---|
| [DuckDB](https://duckdb.org/) | SQL analytics engine — queries the 11 GB CSV in-place |
| [Polars](https://pola.rs/) | High-performance DataFrame library (declared dependency) |
| [Matplotlib](https://matplotlib.org/) + [Seaborn](https://seaborn.pydata.org/) | Visualisation |
| [scikit-learn](https://scikit-learn.org/) | Clustering & anomaly detection (Isolation Forest, K-Means) |
| [SciPy](https://scipy.org/) | Statistical tests |
| [uv](https://docs.astral.sh/uv/) | Python package & project manager |

## License

Dataset is public domain per HHS Open Data policy.
