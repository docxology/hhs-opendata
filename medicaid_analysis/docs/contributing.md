# Contributing Guide

## Project Structure

```
medicaid_analysis/
├── main.py                 # Orchestrator — imports and runs all sections
├── utils/                  # Shared utilities (config, formatting, I/O, DB)
├── eda/                    # Exploratory data analysis
├── stats/                  # Statistical tests and models
├── providers/              # Provider behavior analysis
├── procedures/             # HCPCS / procedure analysis
├── temporal/               # Time-series analysis
├── visualization/          # Deep-dive charts and dashboards
├── fraud/                  # Fraud detection suite
└── docs/                   # Documentation
```

## Adding a New Analysis Section

### 1. Choose the Right Package

| If your analysis is about... | Use package |
|---|---|
| Basic data exploration | `eda/` |
| Statistical tests/models | `stats/` |
| Provider behavior patterns | `providers/` |
| HCPCS code analysis | `procedures/` |
| Time-series / seasonal | `temporal/` |
| Advanced visualizations | `visualization/` |
| Fraud/anomaly detection | `fraud/` |

### 2. Create the Module

```python
"""Package — Section Title (Section NN)."""

import matplotlib.pyplot as plt
from utils import log, banner, query, savefig, usd, OUTPUT_DIR


def sNN_section_name(con, csv: str):
    """One-line description of what this section does."""
    banner(NN, "Section Title")
    
    # SQL query
    df = query(con, f"""
        SELECT ... FROM '{csv}' WHERE ...
    """)
    
    # Analysis
    ...
    
    # Save outputs
    df.to_csv(OUTPUT_DIR / "NN_section_name.csv", index=False)
    log.info("  Key metric: %s", value)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(12, 7))
    ...
    savefig(fig, "NN_section_name.png")
    
    return df
```

### 3. Register in Package `__init__.py`

```python
from .module_name import sNN_section_name
```

### 4. Add to `main.py` Orchestrator

```python
from package_name import sNN_section_name
# ...
if should_run(NN, args):
    run_section(NN, sNN_section_name, con, csv)
```

### 5. Update Documentation

- Add entry to `docs/sections.md`
- Add row to `docs/modules.md`
- If new fraud method: update `docs/fraud_guide.md`

## Code Conventions

1. **Section functions** start with `sNN_` where NN is the section number
2. **All SQL** goes through `query(con, sql)` — never use raw DuckDB calls
3. **All plots** saved via `savefig(fig, name, subdir=None)` — auto-closes figures
4. **All CSVs** saved via `save_csv(df, name, subdir=None)` or `df.to_csv(OUTPUT_DIR / ...)`
5. **Logging** via `log.info(...)` — structured messages with key metrics
6. **Formatting** via `usd_fmt()`, `num_fmt()`, `pct_fmt()` — never raw f-strings for display

## Testing

### Unit & Integration Tests

```bash
# Run the full test suite (93 tests)
uv run python -m pytest tests/ -v

# Run a specific test module
uv run python -m pytest tests/test_utils.py -v
uv run python -m pytest tests/test_sections.py -v
uv run python -m pytest tests/test_imports.py -v
uv run python -m pytest tests/test_main.py -v
```

### End-to-End Pipeline

```bash
# Quick validation with sample data
uv run main.py --sample --sections 1 5 32

# Run single section
uv run main.py --sections NN

# Analyse a custom CSV file
uv run main.py --csv /path/to/custom.csv

# Full pipeline
uv run main.py
```
