# AGENTS.md — `hhs-opendata/medicaid_analysis/procedures`

## What this is

HCPCS (procedure-code) analysis — category breakdowns, co-billing patterns, claims-size distributions, and code lifecycles.

## Layout (verified by direct listing, 2026-08-29)

```
__init__.py, categories.py, claims_size.py, cooccurrence.py, lifecycle.py
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

- All four modules are standalone; no cross-section state required.
- Generated `output/` and `plots/` artifacts are tracked here; `data/*.csv` and `medicaid.db` are git-ignored.
- If the tree changed since 2026-08-29, re-verify the listing above against disk.
