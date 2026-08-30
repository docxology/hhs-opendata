# AGENTS.md — `hhs-opendata/medicaid_analysis/plots`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Generated PNG figures from the 40-section pipeline (`uv run main.py`, run from `medicaid_analysis/`). **Regenerable**. Mirrors the `output/` per-sample-fraction layout: `1pct/`-`100pct/` written by `run_multi_scale.py` via `MEDICAID_PLOTS_DIR`, each with a `fraud/` subfolder; top-level `NN_*.png` and `fraud/` are from the most recent default-output run. Naming: `NN_section_slug.png` matching section numbers in `../README.md`.

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
01_monthly_dashboard.png, 01_monthly_trends.png, 02_yearly_spending.png, 03_top_procedures.png, 04_top_providers.png, 05_cost_distributions.png, 06_anomaly_scatter.png, 06_zscore_by_procedure.png, 07_billing_analysis.png, 08_lorenz_curves.png, 09_correlations.png, 09_pairplot.png, 100pct, 10_procedure_diversity.png, 10pct, 11_temporal_patterns.png, 12_high_value_hcpcs.png, 13_provider_growth.png, 14_category_cost_per_claim.png, 14_hcpcs_categories.png, 15_power_law.png, 16_provider_network.png, 17_qq_plots.png, 18_spending_deciles.png, 19_beneficiary_intensity.png, 1pct, 20_box_violin.png, 21_rolling_cumulative.png, 22_yoy_comparison.png, 23_cooccurrence.png, 24_provider_tenure.png, 25_spending_velocity.png, 26_claims_size.png, 27_specialization.png, 28_outlier_profiles.png, 29_market_share.png, 30_hcpcs_lifecycle.png, 31_benfords_law.png, 32_executive_summary.png, 50pct, fraud
```

## Gotchas

- Generated artifacts: safe to delete and regenerate; do not hand-edit.
- A few legacy duplicates exist in `output/` (e.g. `11_seasonality.csv` and
  `11_temporal_patterns.csv` alongside `11_seasonal_patterns.csv`) from earlier
  section-naming iterations — current sections write the canonical names.
- Never `git add` anything under `projects/ongoing/`.
