# AGENTS.md — `hhs-opendata/medicaid_analysis/fraud`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Fraud detection suite — sections S33-S40: six independent detection methods (upcoding, billing velocity, phantom billing, behavioral clustering, cost outliers, relationship anomalies, temporal anomalies) plus S40, which combines all signals into a composite per-provider risk score and tier.

## Layout (verified by direct listing, 2026-08-29)

```
__init__.py, clustering.py, composite.py, cost_outliers.py, phantom.py, relationships.py, temporal.py, upcoding.py, velocity.py
```

## Invariants

- Every module exposes one `sNN_*` section function imported by `main.py`;
  the section number is in the module docstring. Adding a section means:
  new module, re-export in `__init__.py`, dispatch in `main.py`, entry in
  `docs/sections.md` and `docs/modules.md`, and a signature row in
  `tests/test_imports.py` SECTION_REGISTRY.
- DuckDB-first: heavy aggregation happens in SQL against the CSV, never a
  full pandas load.
- Outputs go to `OUTPUT_DIR` / `PLOTS_DIR` (env-overridable via
  `MEDICAID_OUTPUT_DIR` / `MEDICAID_PLOTS_DIR`), named `NN_<slug>.csv/.png`.

## Gotchas

- S40 requires the outputs of S33-S39 as inputs (see `composite.py`: `s40_composite_fraud_score(con, csv, upcoding_df, velocity_df, phantom_df, cost_outlier_df, relationship_df, temporal_df)`); it is skipped if any upstream fraud section failed. `--skip-fraud` on `main.py`/`run_multi_scale.py` disables S33-S40 entirely.
- Methodology and thresholds: `../docs/fraud_guide.md`.
- Never `git add` anything under `projects/ongoing/` (this repo tracks these
  docs explicitly; data and generated artifacts stay untracked).
- If the tree changed since 2026-08-29, re-verify the listing above against disk.
