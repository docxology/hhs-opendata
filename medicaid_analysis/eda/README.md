# `eda/`

Exploratory Data Analysis — sections S01-S05 and S12: dataset shape and cardinalities, monthly/yearly spending trends, top procedures and providers, cost-per-claim/per-beneficiary efficiency, and high-value claims.

## Sections implemented

- S01 `summary.py` — row counts, date range, unique entities, numeric summaries (returns the shared `eda_result` dict)
- S02 `trends.py` — monthly & yearly spending dashboards
- S03/S04 `top_entities.py` — top HCPCS codes and providers by spend/claims
- S05 `cost_efficiency.py` — cost per claim / per beneficiary distributions (its `cost_df` feeds S06, S09, S17, S20, S28)
- S12 `high_value.py` — highest-value individual records

## Files

- `summary.py` — `s01_eda(con, csv)` -> `01_eda_summary.json`, numeric summaries
- `trends.py` — `s02_monthly_trends`
- `top_entities.py` — `s03_top_procedures`, `s04_top_providers`
- `cost_efficiency.py` — `s05_cost_efficiency`
- `high_value.py` — `s12_high_value_claims`

## Verify

```bash
cd medicaid_analysis
uv run pytest tests/test_sections.py -k s01  # (unverified) needs data/sample.csv
```

Part of the medicaid_analysis pipeline (local-only tree; see `../README.md`).
