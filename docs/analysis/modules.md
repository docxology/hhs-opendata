# Module Reference

## `utils/` — Shared Utilities

| Module | Functions | Purpose |
|---|---|---|
| `config.py` | `log`, paths, constants | Logging, paths, dataset stats |
| `formatting.py` | `usd_fmt`, `usd`, `num_fmt`, `pct_fmt` | Number/currency formatters |
| `io.py` | `savefig`, `save_csv`, `banner` | File I/O, section banners |
| `db.py` | `connect`, `query` | DuckDB connection & SQL helpers |

---

## `eda/` — Exploratory Data Analysis

| Module | Function | Section | Description |
|---|---|---|---|
| `summary.py` | `s01_eda` | S01 | Row counts, date range, unique entities, numeric summaries |
| `trends.py` | `s02_monthly_trends` | S02 | Monthly & yearly spending dashboards |
| `top_entities.py` | `s03_top_procedures` | S03 | Top HCPCS codes by spending/claims |
| `top_entities.py` | `s04_top_providers` | S04 | Top providers by spending/claims |
| `cost_efficiency.py` | `s05_cost_efficiency` | S05 | Cost-per-claim, cost-per-beneficiary metrics |
| `high_value.py` | `s12_high_value_claims` | S12 | Highest-value individual records |

---

## `stats/` — Statistical Analysis

| Module | Function | Section | Description |
|---|---|---|---|
| `anomaly.py` | `s06_anomaly_detection` | S06 | Z-score and IQR anomaly detection |
| `concentration.py` | `s08_concentration` | S08 | Gini, HHI, Lorenz curve analysis |
| `concentration.py` | `s18_spending_deciles` | S18 | Provider spending decile breakdown |
| `correlations.py` | `s09_correlations` | S09 | Correlation matrices (paid/claims/bene) |
| `power_law.py` | `s15_power_law` | S15 | Power-law distribution fitting |
| `distribution_tests.py` | `s17_statistical_tests` | S17 | KS, Shapiro-Wilk, normality tests |
| `benfords_law.py` | `s31_benfords_law` | S31 | Benford's law conformance testing |

---

## `providers/` — Provider Behavior

| Module | Function | Section | Description |
|---|---|---|---|
| `billing.py` | `s07_billing_vs_servicing` | S07 | Billing vs servicing NPI analysis |
| `diversity.py` | `s10_procedure_diversity` | S10 | Procedure breadth per provider |
| `growth.py` | `s13_provider_growth` | S13 | Growth trajectories (early vs late half) |
| `network.py` | `s16_provider_network` | S16 | Billing ↔ servicing relationships |
| `tenure.py` | `s24_provider_tenure` | S24 | Provider longevity & activity rate |
| `specialization.py` | `s27_provider_specialization` | S27 | HHI-based specialization index |
| `market_share.py` | `s29_market_share_dynamics` | S29 | Top-provider market share over time |

---

## `procedures/` — Procedure Analysis

| Module | Function | Section | Description |
|---|---|---|---|
| `categories.py` | `s14_hcpcs_categories` | S14 | HCPCS code prefix category breakdown |
| `cooccurrence.py` | `s23_procedure_cooccurrence` | S23 | Procedure pair co-occurrence analysis |
| `claims_size.py` | `s26_claims_size_distribution` | S26 | Claims size stratification (micro→mega) |
| `lifecycle.py` | `s30_hcpcs_lifecycle` | S30 | Code entry/exit timeline & longevity |

---

## `temporal/` — Temporal Analysis

| Module | Function | Section | Description |
|---|---|---|---|
| `patterns.py` | `s11_temporal_patterns` | S11 | Monthly/quarterly seasonality indices |
| `intensity.py` | `s19_beneficiary_intensity` | S19 | Claims-per-beneficiary utilization |
| `rolling.py` | `s21_rolling_cumulative` | S21 | 3/6/12-month rolling averages & cumulative |
| `yoy.py` | `s22_yoy_comparison` | S22 | Year-over-year spending/claims comparison |
| `velocity.py` | `s25_spending_velocity` | S25 | Monthly velocity & acceleration curves |

---

## `visualization/` — Advanced Visualization

| Module | Function | Section | Description |
|---|---|---|---|
| `distributions.py` | `s20_distribution_deep_dive` | S20 | Box/violin plots by top procedure codes |
| `outliers.py` | `s28_outlier_profiles` | S28 | Multi-dimensional outlier profiling |
| `executive.py` | `s32_executive_summary` | S32 | KPI dashboard with sparklines |

---

## `fraud/` — Fraud Detection

| Module | Function | Section | Description |
|---|---|---|---|
| `upcoding.py` | `s33_upcoding_detection` | S33 | Z-score deviation from peer pricing |
| `velocity.py` | `s34_billing_velocity_anomalies` | S34 | Sudden billing volume spikes |
| `phantom.py` | `s35_phantom_billing` | S35 | Impossible claims/beneficiary ratios |
| `clustering.py` | `s36_provider_clustering` | S36 | K-Means behavioral profiling |
| `cost_outliers.py` | `s37_cost_outliers_by_procedure` | S37 | Within-HCPCS IQR cost outliers |
| `relationships.py` | `s38_billing_servicing_anomalies` | S38 | Concentrated billing relationships |
| `temporal.py` | `s39_temporal_anomalies` | S39 | Low-entropy / high-CV temporal flags |
| `composite.py` | `s40_composite_fraud_score` | S40 | Multi-signal composite risk scoring |
