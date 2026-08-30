# `stats/`

Statistical tests and models — anomalies, concentration, correlations, power law, normality tests, spending deciles, and Benford's Law.

## Sections implemented

- S06 `anomaly.py` — z-score flagging plus Isolation Forest on cost metrics (needs S05 `cost_df`)
- S08/S18 `concentration.py` — Gini/HHI concentration metrics and spending deciles
- S09 `correlations.py` — Pearson/Spearman correlation matrices (needs S05 `cost_df`)
- S15 `power_law.py` — Pareto/power-law fit of spending concentration
- S17 `distribution_tests.py` — normality/statistical tests on cost distributions (needs S05 `cost_df`)
- S31 `benfords_law.py` — first-digit distribution as a fraud signal

## Files

- `anomaly.py` — `s06_anomaly_detection(con, csv, cost_df)`
- `concentration.py` — `s08_concentration`, `s18_spending_deciles`
- `correlations.py` — `s09_correlations`
- `power_law.py` — `s15_power_law`
- `distribution_tests.py` — `s17_statistical_tests`
- `benfords_law.py` — `s31_benfords_law`

## Verify

```bash
cd medicaid_analysis
uv run main.py --sections 6 8 31 --sample  # (unverified - needs sample CSV)
```

Part of the medicaid_analysis pipeline (local-only tree; see `../README.md`).
