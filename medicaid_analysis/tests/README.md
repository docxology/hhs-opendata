# `tests/`

Pytest suite for the medicaid_analysis pipeline: import/signature contract for all
40 section functions, `main.py` CLI behavior, utils helpers, and integration runs
of real sections against the sample dataset.

## Run

```bash
cd medicaid_analysis
uv run pytest            # testpaths=tests, pythonpath=. (set in pyproject.toml)
uv run pytest tests/test_sections.py -v   # integration - skips if data/sample.csv is absent
```

## Files

- `test_imports.py` — asserts every `sNN_*` function exists with its expected signature (SECTION_REGISTRY)
- `test_main.py` — `main.py --help` and argument-parsing defaults (subprocess)
- `test_sections.py` — integration: runs sections on `data/sample.csv` and checks output CSV/PNG artifacts appear; module-scoped fixtures skip cleanly when the sample CSV is absent
- `test_utils.py` — config paths, formatting, I/O helpers

Part of the medicaid_analysis subproject. Parent: `../README.md`.
