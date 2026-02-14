# Architecture Guide

## Design Principles

1. **Modular Subpackages** — Each analytical domain is a self-contained Python package
2. **Shared Utilities** — Common config, formatting, I/O, and DB helpers in `utils/`
3. **Section Independence** — Each analysis section (S01–S40) can run independently
4. **CLI Orchestration** — `main.py` dispatches sections with timing, error handling, and selective execution
5. **DuckDB-First Queries** — Heavy SQL computation via DuckDB for out-of-core performance

## Package Dependency Graph

```
main.py (orchestrator)
  ├── utils/          ← all packages depend on this
  ├── eda/            ← standalone
  ├── stats/          ← standalone
  ├── providers/      ← standalone
  ├── procedures/     ← standalone
  ├── temporal/       ← standalone
  ├── visualization/  ← depends on eda (cost_df), temporal (yoy_totals)
  └── fraud/          ← S40 depends on S33-S39 outputs
```

## Data Flow

```
CSV file (DuckDB reads directly)
    ↓
DuckDB SQL queries (via utils.query)
    ↓
pandas DataFrames (analysis/transforms)
    ↓
CSV outputs (utils.save_csv → output/)
Visualization (utils.savefig → plots/)
```

## Module Organization

Each subpackage follows a consistent pattern:

```python
# module_name.py
"""Docstring with section description."""
import ... from utils import log, banner, query, savefig, ...

def sXX_section_name(con, csv: str):
    """Section-level docstring."""
    banner(XX, "Section Title")
    # SQL query via DuckDB
    df = query(con, f"SELECT ... FROM '{csv}' ...")
    # Analysis & transforms
    ...
    # Save outputs
    df.to_csv(OUTPUT_DIR / "XX_filename.csv", index=False)
    savefig(fig, "XX_filename.png")
    return result
```

## Error Handling

The orchestrator wraps each section in `run_section()`, which:

- Times execution
- Catches and logs exceptions without halting the pipeline
- Returns `None` on failure so downstream sections can degrade gracefully

## Configuration

All paths and constants live in `utils/config.py`:

- `BASE_DIR` — Project root (auto-detected via `__file__`)
- `DATA_DIR` — Parent `data/` directory
- `OUTPUT_DIR` — CSV output directory
- `PLOTS_DIR` — Plot output directory
- `FULL_CSV` / `SAMPLE_CSV` — Dataset paths
