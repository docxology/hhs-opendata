# AGENTS.md — `hhs-opendata/medicaid_analysis/utils`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Shared utilities for every subpackage — configuration/paths/dataset constants, DuckDB helpers, output I/O, and number formatting.

## Layout (verified by direct listing, 2026-08-29)

```
__init__.py, config.py, db.py, formatting.py, io.py
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

- `OUTPUT_DIR`/`PLOTS_DIR` come from env vars `MEDICAID_OUTPUT_DIR`/`MEDICAID_PLOTS_DIR` when set (this is how `run_multi_scale.py` redirects per-scale output); otherwise they default to this package's `output/` and `plots/`.
- `FULL_*` constants in `config.py` are reference statistics of the full dataset, not live query results.
- Never `git add` anything under `projects/ongoing/` (this repo tracks these
  docs explicitly; data and generated artifacts stay untracked).
- If the tree changed since 2026-08-29, re-verify the listing above against disk.
