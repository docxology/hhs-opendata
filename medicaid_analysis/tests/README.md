# Medicaid analysis tests

Run from the repository root. Pytest loads the settings in
[`medicaid_analysis/pyproject.toml`](../pyproject.toml), and the CLI tests find
`main.py` in the analysis project.

```bash
cd medicaid_analysis
uv run --locked python -m pytest tests/ -rs
```

| Test module | Coverage |
| --- | --- |
| [`test_imports.py`](test_imports.py) | Imports and signatures for the registered analysis sections. |
| [`test_main.py`](test_main.py) | CLI help, argument defaults and section selection. |
| [`test_sections.py`](test_sections.py) | Analysis sections and artifacts produced from the real sample CSV. |
| [`test_utils.py`](test_utils.py) | Configured paths, formatting, DuckDB, CSV and figure helpers. |

The section tests and CSV-query test require `data/sample.csv` at the repository
root. To prepare it from the downloaded HHS CSV, follow the
[contributing guide](../../docs/analysis/contributing.md#unit-and-integration-tests).
Use `MEDICAID_OUTPUT_DIR` and `MEDICAID_PLOTS_DIR` to direct test artifacts to
scratch directories when you want to keep the normal analysis output separate.
