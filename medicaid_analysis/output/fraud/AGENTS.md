# AGENTS.md — `hhs-opendata/medicaid_analysis/output/fraud`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Fraud-analysis CSV outputs (sections S33-S40) from a default-output pipeline run (`uv run main.py`). Regenerable — S33 upcoding, S34 velocity, S35 phantom, S36 clustering, S37 cost outliers, S38 relationships, S39 temporal, S40 composite risk score/tiers.

## Layout (verified by direct listing, 2026-08-29)

```
33_upcoding_all.csv, 33_upcoding_flagged.csv, 34_spike_events.csv, 34_velocity_anomalies.csv, 35_phantom_providers.csv, 35_phantom_records.csv, 36_cluster_stats.csv, 36_provider_clusters.csv, 37_cost_outlier_providers.csv, 37_cost_outlier_records.csv, 38_billing_servicing_anomalies.csv, 39_temporal_flagged.csv, 39_temporal_profiles.csv, 40_fraud_risk_scores.csv, 40_high_risk_providers.csv, 40_risk_tier_summary.csv
```

## Gotchas

- Generated artifacts (regenerable via the S33-S40 sections of `main.py`);
  do not hand-edit. Never `git add` anything under `projects/ongoing/`.
