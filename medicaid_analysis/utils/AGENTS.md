# AGENTS.md — `hhs-opendata/medicaid_analysis/utils`

## What this is

Shared utilities for every subpackage — configuration/paths/dataset constants, DuckDB helpers, output I/O, and number formatting.

## Layout (verified by direct listing, 2026-08-29)

```
__init__.py, config.py, db.py, formatting.py, io.py
```

## Invariants

- Helper package only: it defines no `sNN_*` section functions. Analysis
  modules import `log`, `connect`, `query`, `savefig`, and formatting
  helpers from here.
- DuckDB-first: heavy aggregation happens in SQL against the CSV, never a
  full pandas load.
- Outputs go to `OUTPUT_DIR` / `PLOTS_DIR` (env-overridable via
  `MEDICAID_OUTPUT_DIR` / `MEDICAID_PLOTS_DIR`), named `NN_<slug>.csv/.png`.

## Gotchas

- `OUTPUT_DIR`/`PLOTS_DIR` come from env vars `MEDICAID_OUTPUT_DIR`/`MEDICAID_PLOTS_DIR` when set (this is how `run_multi_scale.py` redirects per-scale output); otherwise they default to this package's `output/` and `plots/`.
- `FULL_*` constants in `config.py` are reference statistics of the full dataset, not live query results.
- Generated `output/` and `plots/` artifacts are tracked here; `data/*.csv` and `medicaid.db` are git-ignored.
- If the tree changed since 2026-08-29, re-verify the listing above against disk.
