# AGENTS.md — `hhs-opendata/medicaid_analysis/plots/fraud`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Fraud-analysis PNG plots (sections S33-S40) from a default-output pipeline run (`uv run main.py`). Regenerable — S33 upcoding, S34 velocity, S35 phantom, S36 clustering, S37 cost outliers, S38 relationships, S39 temporal, S40 composite risk score/tiers.

## Layout (verified by direct listing, 2026-08-29)

```
33_upcoding.png, 34_velocity_anomalies.png, 35_phantom_billing.png, 36_provider_clusters.png, 37_cost_outliers.png, 38_billing_servicing.png, 39_temporal_anomalies.png, 40_fraud_risk_scores.png
```

## Gotchas

- Generated artifacts (regenerable via the S33-S40 sections of `main.py`);
  do not hand-edit. Never `git add` anything under `projects/ongoing/`.
