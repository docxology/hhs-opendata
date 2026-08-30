# `visualization/`

Deep-dive charts and dashboards — distribution deep dives, multi-dimensional outlier profiles, and the executive summary dashboard.

## Sections implemented

- S20 `distributions.py` — box/violin distribution deep dive (needs S05 `cost_df`)
- S28 `outliers.py` — multi-dimensional outlier profiles (needs S05 `cost_df`)
- S32 `executive.py` — executive dashboard: KPIs and sparklines (needs S01 `eda` dict + S22 `yoy_totals`)

## Files

- `distributions.py` — `s20_distribution_deep_dive(con, csv, cost_df)`
- `executive.py` — `s32_executive_summary(con, csv, eda, yoy_totals)`
- `outliers.py` — `s28_outlier_profiles(con, csv, cost_df)`

## Verify

```bash
cd medicaid_analysis
uv run main.py --sections 20 28 32 --sample  # (unverified - needs data/sample.csv)
```

Part of the medicaid_analysis pipeline (local-only tree; see `../README.md`).
