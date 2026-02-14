# Section Catalog

Complete listing of all 40 analysis sections with descriptions, inputs, outputs, and dependencies.

## EDA Sections (S01–S05, S12)

### S01 — Exploratory Data Analysis

- **Module**: `eda/summary.py`
- **Outputs**: `01_eda_summary.csv`, `01_eda_summary.json`
- **Description**: Row counts, date range, unique providers/codes, numeric distribution summaries
- **Returns**: `dict` with `row_count`, `total_paid`, `billing_npis`, `hcpcs_codes`, etc.

### S02 — Monthly & Yearly Spending Trends

- **Module**: `eda/trends.py`
- **Outputs**: `02_monthly_trends.csv`, `02_monthly_dashboard.png`, `02_yearly_spending.png`
- **Description**: Multi-metric monthly dashboard (paid, claims, providers, avg cost)

### S03 — Top Procedures

- **Module**: `eda/top_entities.py`
- **Outputs**: `03_top_procedures.csv`, `03_top_procedures.png`

### S04 — Top Providers

- **Module**: `eda/top_entities.py`
- **Outputs**: `04_top_providers.csv`, `04_top_providers.png`

### S05 — Cost Efficiency Metrics

- **Module**: `eda/cost_efficiency.py`
- **Outputs**: `05_cost_efficiency.csv`, `05_cost_efficiency.png`
- **Returns**: `cost_df` DataFrame (used by S20, S28)

### S12 — Highest-Value Records

- **Module**: `eda/high_value.py`
- **Outputs**: `12_high_value.csv`, `12_high_value.png`

---

## Statistics Sections (S06, S08–S09, S15, S17–S18, S31)

### S06 — Anomaly Detection

- **Module**: `stats/anomaly.py`
- **Method**: Z-score + IQR outlier detection on paid amounts
- **Outputs**: `06_anomalies.csv`, `06_anomaly_detection.png`

### S08 — Concentration Analysis

- **Module**: `stats/concentration.py`
- **Method**: Gini coefficient, HHI, Lorenz curve, top-N share
- **Outputs**: `08_concentration.csv`, `08_lorenz_curve.png`

### S09 — Correlations

- **Module**: `stats/correlations.py`
- **Method**: Pearson/Spearman correlation matrices for key metrics
- **Outputs**: `09_correlations.csv`, `09_correlation_matrix.png`

### S15 — Power-Law Distribution

- **Module**: `stats/power_law.py`
- **Method**: Log-log regression, Pareto tail fitting
- **Outputs**: `15_power_law.csv`, `15_power_law.png`

### S17 — Statistical Tests

- **Module**: `stats/distribution_tests.py`
- **Method**: KS test, Shapiro-Wilk, Anderson-Darling, normality assessment
- **Outputs**: `17_statistical_tests.csv`, `17_distribution_tests.png`

### S18 — Spending Deciles

- **Module**: `stats/concentration.py`
- **Method**: Provider spending stratified into 10 deciles
- **Outputs**: `18_spending_deciles.csv`, `18_spending_deciles.png`

### S31 — Benford's Law

- **Module**: `stats/benfords_law.py`
- **Method**: First-digit conformance testing with chi-squared statistic
- **Outputs**: `31_benfords_law.csv`, `31_benfords_law.png`

---

## Provider Sections (S07, S10, S13, S16, S24, S27, S29)

### S07 — Billing vs Servicing

- **Module**: `providers/billing.py`
- **Description**: Same-entity vs third-party billing split
- **Outputs**: `07_billing_vs_servicing.csv`, `07_billing_analysis.png`

### S10 — Procedure Diversity

- **Module**: `providers/diversity.py`
- **Description**: How many HCPCS codes each provider bills
- **Outputs**: `10_procedure_diversity.csv`, `10_procedure_diversity.png`

### S13 — Provider Growth

- **Module**: `providers/growth.py`
- **Description**: Early vs late half spending growth trajectories
- **Outputs**: `13_provider_growth.csv`, `13_provider_growth.png`

### S16 — Provider Network

- **Module**: `providers/network.py`
- **Description**: Billing ↔ servicing NPI relationship graphs
- **Outputs**: `16_billing_to_servicing.csv`, `16_provider_network.png`

### S24 — Provider Tenure

- **Module**: `providers/tenure.py`
- **Description**: Longevity, activity rate, tenure cohort analysis
- **Outputs**: `24_provider_tenure.csv`, `24_provider_tenure.png`

### S27 — Provider Specialization (HHI)

- **Module**: `providers/specialization.py`
- **Description**: Herfindahl-Hirschman Index for procedure concentration
- **Outputs**: `27_provider_hhi.csv`, `27_specialization.png`

### S29 — Market Share Dynamics

- **Module**: `providers/market_share.py`
- **Description**: Top-10 providers' share over time
- **Outputs**: `29_market_share_dynamics.csv`, `29_market_share.png`

---

## Procedure Sections (S14, S23, S26, S30)

### S14 — HCPCS Categories

- **Module**: `procedures/categories.py`
- **Description**: Spending breakdowns by HCPCS code prefix group
- **Outputs**: `14_hcpcs_categories.csv`, `14_hcpcs_categories.png`

### S23 — Procedure Co-occurrence

- **Module**: `procedures/cooccurrence.py`
- **Description**: Which procedures are billed together by the same providers
- **Outputs**: `23_procedure_cooccurrence.csv`, `23_cooccurrence.png`

### S26 — Claims Size Distribution

- **Module**: `procedures/claims_size.py`
- **Description**: Stratification into micro/small/medium/large/mega buckets
- **Outputs**: `26_claims_size_buckets.csv`, `26_claims_size.png`

### S30 — HCPCS Lifecycle

- **Module**: `procedures/lifecycle.py`
- **Description**: When codes appear, disappear, and how long they last
- **Outputs**: `30_hcpcs_lifecycle.csv`, `30_hcpcs_lifecycle.png`

---

## Temporal Sections (S11, S19, S21–S22, S25)

### S11 — Temporal Patterns

- **Module**: `temporal/patterns.py`
- **Description**: Monthly/quarterly seasonal indices and provider counts
- **Outputs**: `11_seasonal_patterns.csv`, `11_temporal_patterns.png`

### S19 — Beneficiary Intensity

- **Module**: `temporal/intensity.py`
- **Description**: Claims-per-beneficiary utilization analysis
- **Outputs**: `19_beneficiary_intensity.csv`, `19_beneficiary_intensity.png`

### S21 — Rolling & Cumulative

- **Module**: `temporal/rolling.py`
- **Description**: 3/6/12-mo rolling averages, cumulative spending, volatility
- **Outputs**: `21_rolling_cumulative.csv`, `21_rolling_cumulative.png`

### S22 — Year-over-Year Comparison

- **Module**: `temporal/yoy.py`
- **Description**: Annual spending/claims overlays and YoY growth rates
- **Outputs**: `22_yoy_totals.csv`, `22_yoy_comparison.png`
- **Returns**: `yoy_totals` DataFrame (used by S32)

### S25 — Spending Velocity

- **Module**: `temporal/velocity.py`
- **Description**: Month-over-month velocity (Δ$) and acceleration (ΔΔ$)
- **Outputs**: `25_spending_velocity.csv`, `25_spending_velocity.png`

---

## Visualization Sections (S20, S28, S32)

### S20 — Distribution Deep-Dive

- **Module**: `visualization/distributions.py`
- **Depends on**: S05 (`cost_df`)
- **Outputs**: `20_procedure_percentiles.csv`, `20_box_violin.png`

### S28 — Outlier Profiles

- **Module**: `visualization/outliers.py`
- **Depends on**: S05 (`cost_df`)
- **Outputs**: `28_multi_dim_outliers.csv`, `28_outlier_profiles.png`

### S32 — Executive Summary Dashboard

- **Module**: `visualization/executive.py`
- **Depends on**: S01 (`eda_result`), S22 (`yoy_totals`)
- **Outputs**: `32_executive_summary.png`

---

## Fraud Sections (S33–S40)

### S33 — Upcoding Detection

- **Module**: `fraud/upcoding.py`
- **Method**: Per-provider z-score deviation from peer cost-per-claim
- **Flags**: avg_z > 1.5 or upcode ratio > 50%
- **Outputs**: `fraud/33_upcoding_flagged.csv`, `fraud/33_upcoding.png`

### S34 — Billing Velocity Anomalies

- **Module**: `fraud/velocity.py`
- **Method**: Rolling 3-month mean; spike if >5x or z>4
- **Outputs**: `fraud/34_velocity_anomalies.csv`, `fraud/34_velocity_anomalies.png`

### S35 — Phantom Billing

- **Module**: `fraud/phantom.py`
- **Method**: Claims/beneficiary ratio vs peer P95; flag if >3x or >50 absolute
- **Outputs**: `fraud/35_phantom_providers.csv`, `fraud/35_phantom_billing.png`

### S36 — Provider Clustering

- **Module**: `fraud/clustering.py`
- **Method**: K-Means (k=6) on log-scaled behavioral features
- **Outputs**: `fraud/36_provider_clusters.csv`, `fraud/36_provider_clusters.png`

### S37 — Cost Outliers by Procedure

- **Module**: `fraud/cost_outliers.py`
- **Method**: IQR fence (Q3 + 3×IQR) + excess ratio >3x median
- **Outputs**: `fraud/37_cost_outlier_providers.csv`, `fraud/37_cost_outliers.png`

### S38 — Billing-Servicing Anomalies

- **Module**: `fraud/relationships.py`
- **Method**: Concentration >90% + high volume, or broad code sharing
- **Outputs**: `fraud/38_billing_servicing_anomalies.csv`, `fraud/38_billing_servicing.png`

### S39 — Temporal Anomalies

- **Module**: `fraud/temporal.py`
- **Method**: Shannon entropy (P5) + coefficient of variation (>2)
- **Outputs**: `fraud/39_temporal_flagged.csv`, `fraud/39_temporal_anomalies.png`

### S40 — Composite Fraud Risk Score

- **Module**: `fraud/composite.py`
- **Depends on**: S33–S39 flag DataFrames
- **Method**: Sum of 6 binary risk signals → Clean/Low/Medium/High tiers
- **Outputs**: `fraud/40_fraud_risk_scores.csv`, `fraud/40_fraud_risk_scores.png`
