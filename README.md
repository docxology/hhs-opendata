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
- **Raw size:** ~11 GB CSV (~3.4 GB compressed)

## Repository Layout

```
hhs-opendata/
├── README.md               ← this file
├── AGENTS.md               ← guidelines for AI agents
├── data/
│   └── medicaid-provider-spending.csv   ← raw dataset (git-ignored)
└── medicaid_analysis/
    ├── pyproject.toml       ← uv project config & deps
    ├── analysis.py          ← main analysis script
    ├── plots/               ← generated visualisations
    └── output/              ← generated summary CSVs
```

## Quick Start

```bash
# 1. Install dependencies (requires uv)
cd medicaid_analysis
uv sync

# 2. Run full analysis
uv run analysis.py

# Output is written to medicaid_analysis/plots/ and medicaid_analysis/output/
```

## Analysis Contents

1. **Exploratory Data Analysis** — row counts, value distributions, date range verification
2. **Monthly Spending Trends** — total paid aggregated by month with line plot
3. **Top Procedures** — HCPCS codes ranked by total Medicaid spend
4. **Top Providers** — NPIs ranked by total billing volume and spend
5. **Cost Efficiency Metrics** — cost-per-claim and cost-per-beneficiary distributions
6. **Anomaly Detection** — z-score flagging of outlier provider-procedure pairs
7. **Billing vs Servicing Provider Analysis** — prevalence of third-party billing

## Technology

| Tool | Purpose |
|---|---|
| [DuckDB](https://duckdb.org/) | SQL analytics engine — queries the 11 GB CSV in-place |
| [Polars](https://pola.rs/) | High-performance DataFrame library |
| [Matplotlib](https://matplotlib.org/) + [Seaborn](https://seaborn.pydata.org/) | Visualisation |
| [scikit-learn](https://scikit-learn.org/) | Statistical analysis & anomaly detection |
| [uv](https://docs.astral.sh/uv/) | Python package & project manager |

## License

Dataset is public domain per HHS Open Data policy.
