# AGENTS.md — `hhs-opendata/medicaid_analysis/stats`

## What this is

Statistical tests and models — anomalies, concentration, correlations, power law, normality tests, spending deciles, and Benford's Law.

## Layout (verified by direct listing, 2026-08-29)

```
__init__.py, anomaly.py, benfords_law.py, concentration.py, correlations.py, distribution_tests.py, power_law.py
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

- S06, S09, S17 depend on the `cost_df` produced by S05; run S05 first (or all sections) or the orchestrator skips them with a warning.
- Generated `output/` and `plots/` artifacts are tracked here; `data/*.csv` and `medicaid.db` are git-ignored.
- If the tree changed since 2026-08-29, re-verify the listing above against disk.
