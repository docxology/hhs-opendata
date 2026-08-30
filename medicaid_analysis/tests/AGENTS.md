# AGENTS.md — `hhs-opendata/medicaid_analysis/tests`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Pytest suite for the pipeline (imports/signatures, CLI behavior, utils,
sample-data integration). Run from `medicaid_analysis/` with `uv run pytest`
(pyproject sets `pythonpath=["."]` and `testpaths=["tests"]`).

## Layout (verified by direct listing, 2026-08-29)

```
__init__.py, test_imports.py, test_main.py, test_sections.py, test_utils.py
```

## Invariants

- `test_imports.py` SECTION_REGISTRY is the signature contract for all 40
  sections; update it in the same change that adds/changes a section function.
- Integration tests (`test_sections.py`) **skip** when `data/sample.csv` is
  absent — an empty-looking pass may just mean no sample data; check the skip count.
- Tests write real artifacts into `output/`/`plots/` via the shared `OUTPUT_DIR`/`PLOTS_DIR`; they are integration tests, not unit-isolated.

## Gotchas

- Run pytest from `medicaid_analysis/` (pythonpath relies on the local pyproject).
- If the tree changed since 2026-08-29, re-verify the listing above against disk.
