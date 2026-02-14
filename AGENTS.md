# AGENTS.md — AI Agent Guidelines

## Project Context

This repository analyses the **Medicaid Provider Spending** dataset from HHS Open Data.

- **Dataset URL:** <https://opendata.hhs.gov/datasets/medicaid-provider-spending/>
- **Raw data path:** `data/medicaid-provider-spending.csv` (~11 GB, git-ignored)
- **Analysis code:** `medicaid_analysis/`

## Data Schema

| Column | Type | Notes |
|---|---|---|
| `BILLING_PROVIDER_NPI_NUM` | string | 10-digit NPI; may differ from servicing provider |
| `SERVICING_PROVIDER_NPI_NUM` | string | 10-digit NPI of the provider who delivered the service |
| `HCPCS_CODE` | string | Procedure code — look up at <https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system> |
| `CLAIM_FROM_MONTH` | date | Always first of the month (`YYYY-MM-01`); range 2018-01 to 2024-12 |
| `TOTAL_UNIQUE_BENEFICIARIES` | integer | Per provider-procedure-month; subject to small-cell suppression |
| `TOTAL_CLAIMS` | integer | Aggregated claim count |
| `TOTAL_PAID` | float | USD; represents Medicaid reimbursement, not patient cost |

## Environment

- **Package manager:** `uv` (all commands run via `uv run`)
- **Python:** ≥ 3.12
- **Primary query engine:** DuckDB (SQL queries against the CSV directly)
- **Key libraries:** polars, pandas, matplotlib, seaborn, scikit-learn

## Conventions

1. **No mocks or fake data** — all analysis uses the real dataset.
2. **DuckDB for heavy lifting** — the CSV is too large for naive pandas reads; always use DuckDB or Polars lazy scanning.
3. **Output directories:**
   - `medicaid_analysis/plots/` — PNG visualisations
   - `medicaid_analysis/output/` — summary CSV/Parquet files
4. **Logging** — all scripts should log progress to stdout with timestamps.
5. **Reproducibility** — pinned dependencies via `uv.lock`; analysis scripts are deterministic.

## Key Analysis Questions

- What are the monthly and yearly spending trends?
- Which HCPCS codes account for the most Medicaid spending?
- Which providers (NPIs) bill the most, and do billing patterns vary by procedure?
- Are there statistical outliers (z-score > 3) in cost-per-beneficiary within specific procedure codes?
- How prevalent is third-party billing (billing NPI ≠ servicing NPI)?

## Working with the Data

```sql
-- Example: DuckDB query against the raw CSV
SELECT HCPCS_CODE, SUM(TOTAL_PAID) as total
FROM 'data/medicaid-provider-spending.csv'
GROUP BY HCPCS_CODE
ORDER BY total DESC
LIMIT 10;
```

```python
# Example: Polars lazy scan
import polars as pl
lf = pl.scan_csv("data/medicaid-provider-spending.csv")
top = lf.group_by("HCPCS_CODE").agg(pl.col("TOTAL_PAID").sum()).sort("TOTAL_PAID", descending=True).head(10).collect()
```

## File Responsibilities

| File | Purpose |
|---|---|
| `README.md` | Project overview and quick start |
| `AGENTS.md` | This file — AI agent context |
| `medicaid_analysis/analysis.py` | Full analysis pipeline |
| `medicaid_analysis/pyproject.toml` | Dependencies and project metadata |
