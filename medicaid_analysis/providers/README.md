# `providers/`

Provider-level behavior analysis — how billing and servicing NPIs differ, and how provider portfolios evolve.

## Sections implemented

- S07 `billing.py` — billing vs servicing provider analysis (third-party billing prevalence)
- S10 `diversity.py` — procedure diversity per provider
- S13 `growth.py` — provider growth trajectories over time
- S16 `network.py` — billing-servicing network analysis
- S24 `tenure.py` — provider tenure & longevity cohorts
- S27 `specialization.py` — specialization summary + provider HHI
- S29 `market_share.py` — market-share dynamics

## Files

- `billing.py` — `s07_billing_vs_servicing`
- `diversity.py` — `s10_procedure_diversity`
- `growth.py` — `s13_provider_growth`
- `network.py` — `s16_provider_network`
- `tenure.py` — `s24_provider_tenure`
- `specialization.py` — `s27_provider_specialization`
- `market_share.py` — `s29_market_share_dynamics`

## Verify

```bash
cd medicaid_analysis
uv run main.py --sections 7 10 13 --sample  # (unverified - needs data/sample.csv)
```

Part of the medicaid_analysis pipeline (local-only tree; see `../README.md`).
