# `temporal/`

Time-series analysis — seasonality, beneficiary intensity, rolling/cumulative metrics, year-over-year comparisons, and spending velocity.

## Sections implemented

- S11 `patterns.py` — day-of-week / month / seasonal spending patterns
- S19 `intensity.py` — beneficiaries per claim intensity
- S21 `rolling.py` — rolling & cumulative spending metrics
- S22 `yoy.py` — year-over-year monthly/total comparisons (its `yoy_totals` feeds S32)
- S25 `velocity.py` — spending velocity over time

## Files

- `intensity.py` — `s19_beneficiary_intensity`
- `patterns.py` — `s11_temporal_patterns`
- `rolling.py` — `s21_rolling_cumulative`
- `velocity.py` — `s25_spending_velocity`
- `yoy.py` — `s22_yoy_comparison`

## Verify

```bash
cd medicaid_analysis
uv run main.py --sections 11 22 25 --sample  # (unverified - needs data/sample.csv)
```

Part of the medicaid_analysis pipeline (local-only tree; see `../README.md`).
