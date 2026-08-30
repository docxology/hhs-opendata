# AGENTS.md — `hhs-opendata/medicaid_analysis/output`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Generated analysis artifacts from the 40-section pipeline (`uv run main.py`, run from `medicaid_analysis/`). **Regenerable** — delete and re-run the pipeline to recreate; nothing here is hand-authored. `1pct/`-`100pct/` hold per-sample-fraction runs (written by `run_multi_scale.py` via the `MEDICAID_OUTPUT_DIR`/`MEDICAID_PLOTS_DIR` env vars), each with its own `fraud/` subfolder; the top-level `NN_*.csv` files and `fraud/` are from the most recent default-output run. Naming: `NN_section_slug.csv` matching the section numbers in `../README.md`.

## Provenance

Everything here is **generated** by `main.py` (default output dirs) or
`run_multi_scale.py` (per-scale subfolders, via `MEDICAID_OUTPUT_DIR` /
`MEDICAID_PLOTS_DIR`). Regenerate with:

```bash
cd medicaid_analysis
uv run main.py --sample                          # default output/ + plots/
uv run run_multi_scale.py --scales 1 10 50 100   # -> output/<label>/ + plots/<label>/
```

## Layout (verified by direct listing, 2026-08-29)

```
01_eda_summary.json, 01_numeric_summary.csv, 01_summary_statistics.csv, 02_monthly_spending.csv, 02_monthly_trends.csv, 02_yearly_summary.csv, 03_top_procedures.csv, 04_top_providers.csv, 05_cost_efficiency_percentiles.csv, 06a_anomalies_zscore.csv, 06b_anomalies_isolation_forest.csv, 07_billing_monthly_by_type.csv, 07_billing_vs_servicing.csv, 08_concentration_metrics.csv, 09_correlation_pearson.csv, 09_correlation_spearman.csv, 100pct, 10_procedure_diversity.csv, 10pct, 11_seasonal_patterns.csv, 11_seasonality.csv, 11_temporal_patterns.csv, 12_highest_value_records.csv, 13_provider_growth.csv, 14_hcpcs_categories.csv, 15_pareto_stats.csv, 16_billing_to_servicing.csv, 16_servicing_to_billing.csv, 17_statistical_tests.csv, 18_spending_deciles.csv, 19_beneficiary_intensity.csv, 1pct, 20_procedure_percentiles.csv, 21_rolling_cumulative.csv, 22_yoy_monthly.csv, 22_yoy_totals.csv, 23_procedure_cooccurrence.csv, 24_cohort_summary.csv, 24_provider_tenure.csv, 25_spending_velocity.csv, 26_claims_size_buckets.csv, 27_provider_hhi.csv, 27_specialization_summary.csv, 28_multi_dim_outliers.csv, 29_market_share_dynamics.csv, 30_hcpcs_lifecycle.csv, 31_benford_stats.csv, 31_benfords_law.csv, 50pct, fraud
```

## Gotchas

- Generated artifacts: safe to delete and regenerate; do not hand-edit.
- A few legacy duplicates exist in `output/` (e.g. `11_seasonality.csv` and
  `11_temporal_patterns.csv` alongside `11_seasonal_patterns.csv`) from earlier
  section-naming iterations — current sections write the canonical names.
- Never `git add` anything under `projects/ongoing/`.
