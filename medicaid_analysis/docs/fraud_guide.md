# Fraud Detection Guide

## Overview

The fraud detection module (sections 33–40) implements six independent detection methods plus a composite scoring system. Each method flags suspicious providers from a different analytical angle, and the composite scorer combines all signals.

## Detection Methods

### 1. Upcoding Detection (S33)

**Question**: Which providers systematically bill more expensive codes than their peers?

**Methodology**:

- For each HCPCS code with ≥20 providers, compute `peer_avg_cpc` and `peer_std_cpc`
- Calculate each provider's z-score: `(provider_cpc - peer_avg) / peer_std`
- Aggregate z-scores per provider across all their codes
- **Flag if**: `avg_z_score > 1.5` OR `upcode_ratio > 0.5` (fraction of codes >2σ)

**Interpretation**: Consistently high z-scores indicate billing at rates well above peers for the same procedures — a classic upcoding signal.

---

### 2. Billing Velocity Anomalies (S34)

**Question**: Which providers had sudden, unexplained spikes in billing volume?

**Methodology**:

- Compute 3-month rolling mean and std per provider
- `spike_ratio = monthly_paid / rolling_mean`
- `z_spike = (monthly_paid - rolling_mean) / rolling_std`
- **Flag if**: `spike_ratio > 5` OR `z_spike > 4`

**Interpretation**: A 5x spike over the rolling average suggests a sudden behavior change — new fraud scheme, billing error, or legitimate practice change that warrants investigation.

---

### 3. Phantom / Ghost Billing (S35)

**Question**: Are any providers billing impossibly high claims-per-beneficiary ratios?

**Methodology**:

- For each provider-HCPCS pair, compute `claims_per_bene`
- Compare to peer P95 for the same HCPCS code
- **Flag if**: `ratio_to_P95 > 3` OR `claims_per_bene > 50` (absolute cap)

**Interpretation**: A provider billing 3x the 95th percentile of claims per beneficiary for a given procedure may be fabricating claims or double-billing.

---

### 4. Provider Clustering (S36)

**Question**: Do any providers form unusual behavioral clusters?

**Methodology**:

- Feature set: `total_paid, total_claims, total_bene, n_codes, active_months, avg_cpc, n_servicing`
- Log-transform → StandardScaler → K-Means (k=6)
- Smallest/most-isolated clusters may represent anomalous provider profiles

**Interpretation**: Unsupervised profiling reveals natural groupings. Providers in small, high-spending clusters with unusual feature combinations deserve closer scrutiny.

---

### 5. Within-HCPCS Cost Outliers (S37)

**Question**: Which providers charge far more than peers for the exact same procedure?

**Methodology**:

- Compute per-HCPCS IQR: `upper_fence = Q3 + 3 × IQR`
- `excess_ratio = provider_cpc / median_cpc`
- **Flag if**: `provider_cpc > upper_fence` AND `excess_ratio > 3`

**Interpretation**: Charging 3x the median for the same HCPCS code (and above the Tukey fence) indicates pricing anomalies — potential fraud, waste, or abuse.

---

### 6. Billing-Servicing Relationship Anomalies (S38)

**Question**: Are there suspicious financial relationships between billing and servicing entities?

**Methodology**:

- For each billing-servicing NPI pair, compute `concentration_pct` (share of billing entity's total)
- **Flag concentrated**: >90% of billing through single servicing provider + >$10K
- **Flag broad**: Shared HCPCS codes > P95 threshold across all pairs

**Interpretation**: A billing entity routing >90% of its volume through a single servicing provider may signal kickback arrangements or shell company structures.

---

### 7. Temporal Anomalies (S39)

**Question**: Do any providers have suspicious temporal billing patterns?

**Methodology**:

- Shannon entropy of monthly billing distribution (lower = more concentrated)
- Coefficient of variation of monthly amounts
- **Flag if**: `entropy < P5` (among providers with ≥6 active months) OR `CV > 2`

**Interpretation**: Very low temporal entropy (billing concentrated in few months) combined with high amounts suggests "hit-and-run" billing patterns.

---

## Composite Scoring (S40)

The composite scorer combines all six detection methods into a single risk tier:

| Score | Tier | Meaning |
|---|---|---|
| 0 | Clean | No fraud signals detected |
| 1 | Low | Single signal — likely noise or edge case |
| 2 | Medium | Multiple signals — warrants review |
| 3+ | High | Strong multi-signal correlation — priority investigation |

**Visualization**: A heatmap shows which specific signals were triggered for the top-50 highest-risk providers, enabling targeted investigation.

## Configurable Thresholds

All thresholds are embedded in their respective modules as constants within the SQL queries or Python logic. To adjust sensitivity:

| Parameter | Default | Module | Effect |
|---|---|---|---|
| Upcoding z-score | 1.5 | `fraud/upcoding.py` | Lower = more flags |
| Spike ratio | 5× | `fraud/velocity.py` | Lower = more flags |
| Phantom claims/bene | 50 | `fraud/phantom.py` | Lower = more flags |
| Cost excess ratio | 3× | `fraud/cost_outliers.py` | Lower = more flags |
| Concentration % | 90% | `fraud/relationships.py` | Lower = more flags |
| Temporal CV | 2.0 | `fraud/temporal.py` | Lower = more flags |
