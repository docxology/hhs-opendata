# AGENTS.md — `hhs-opendata/medicaid_analysis/temporal`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Time-series analysis — seasonality, beneficiary intensity, rolling/cumulative metrics, year-over-year comparisons, and spending velocity.

## Layout (verified by direct listing, 2026-08-29)

```
__init__.py, intensity.py, patterns.py, rolling.py, velocity.py, yoy.py
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

- S22's `yoy_totals` return value is consumed by S32 (executive dashboard); run S22 before S32 or S32 receives `None`.
- Never `git add` anything under `projects/ongoing/` (this repo tracks these
  docs explicitly; data and generated artifacts stay untracked).
- If the tree changed since 2026-08-29, re-verify the listing above against disk.
