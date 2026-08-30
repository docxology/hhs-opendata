# `procedures/`

HCPCS (procedure-code) analysis — category breakdowns, co-billing patterns, claims-size distributions, and code lifecycles.

## Sections implemented

- S14 `categories.py` — HCPCS code categories and category-level cost per claim
- S23 `cooccurrence.py` — procedures commonly billed together by the same provider
- S26 `claims_size.py` — claims-size distribution buckets
- S30 `lifecycle.py` — HCPCS code entry/exit and volume lifecycle

## Files

- `categories.py` — `s14_hcpcs_categories`
- `cooccurrence.py` — `s23_procedure_cooccurrence`
- `claims_size.py` — `s26_claims_size_distribution`
- `lifecycle.py` — `s30_hcpcs_lifecycle`

## Verify

```bash
cd medicaid_analysis
uv run main.py --sections 14 23 26 30 --sample  # (unverified - needs data/sample.csv)
```

Part of the medicaid_analysis pipeline (local-only tree; see `../README.md`).
