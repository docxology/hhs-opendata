# `fraud/`

Fraud detection suite — sections S33-S40: six independent detection methods (upcoding, billing velocity, phantom billing, behavioral clustering, cost outliers, relationship anomalies, temporal anomalies) plus S40, which combines all signals into a composite per-provider risk score and tier.

## Sections implemented

- S33 `upcoding.py` — providers billing systematically higher-cost codes than peers (z-score per HCPCS)
- S34 `velocity.py` — sudden billing-volume spikes / spike events
- S35 `phantom.py` — impossible claims-to-beneficiary ratios
- S36 `clustering.py` — K-Means behavioral profiling of providers
- S37 `cost_outliers.py` — within-HCPCS IQR cost outliers
- S38 `relationships.py` — concentrated billing-servicing pair anomalies
- S39 `temporal.py` — low-entropy / high-CV temporal billing patterns
- S40 `composite.py` — multi-signal composite fraud score -> Clean/Low/Medium/High tiers

## Files

- `clustering.py`, `composite.py`, `cost_outliers.py`, `phantom.py`, `relationships.py`, `temporal.py`, `upcoding.py`, `velocity.py`

## Verify

```bash
cd medicaid_analysis
uv run main.py --sections 33 34 35 40 --sample  # (unverified - needs data/sample.csv)
```

Part of the medicaid_analysis pipeline (local-only tree; see `../README.md`).
