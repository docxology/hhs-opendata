# `utils/`

Shared utilities for every subpackage — configuration/paths/dataset constants, DuckDB helpers, output I/O, and number formatting.

## Sections implemented

n/a (infrastructure package, no analysis sections)

## Files

- `config.py` — paths (`BASE_DIR`, `DATA_DIR`, `FULL_CSV`, `SAMPLE_CSV`, `OUTPUT_DIR`, `PLOTS_DIR`), logging, known full-dataset constants (227,083,361 rows; ~$1.09T paid)
- `db.py` — `connect()` (in-memory DuckDB), `query()`
- `io.py` — `savefig`, `save_csv`, `banner`
- `formatting.py` — `usd`, `usd_fmt`, `num_fmt`, `pct_fmt`

## Verify

```bash
cd medicaid_analysis
uv run pytest tests/test_utils.py -v
```

Part of the medicaid_analysis pipeline (local-only tree; see `../README.md`).
