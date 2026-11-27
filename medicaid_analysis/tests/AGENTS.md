# Medicaid analysis test guide

Use the [test index](README.md) for the supported commands and module map.
Run from `medicaid_analysis/` so pytest reads the package configuration and
`test_main.py` can invoke `main.py`.

- Update `SECTION_REGISTRY` in [`test_imports.py`](test_imports.py) when a
  registered section’s signature changes.
- Keep configured-path tests runnable from a clean checkout. The raw CSV and
  `data/sample.csv` are local inputs.
- Use real files and queries. Check pytest’s skip summary for sample-backed
  tests, and use the output overrides described in the test index when retaining
  any existing analysis outputs.
