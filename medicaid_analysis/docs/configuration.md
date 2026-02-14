# Configuration Guide

## Environment Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
cd medicaid_analysis
uv sync
```

## Directory Structure

All paths are auto-configured in `utils/config.py` relative to the project root:

| Path | Purpose | Default |
|---|---|---|
| `BASE_DIR` | Project root | Auto-detected via `__file__` |
| `DATA_DIR` | Raw CSV data | `../data/` |
| `OUTPUT_DIR` | Generated CSVs | `./output/` |
| `PLOTS_DIR` | Generated plots | `./plots/` |
| `FULL_CSV` | Full dataset | `../data/medicaid-provider-spending.csv` |
| `SAMPLE_CSV` | Sample dataset | `../data/sample.csv` |

## CLI Options

```
usage: main.py [-h] [--sections [SECTIONS ...]] [--skip-fraud] [--sample] [--csv CSV]

Options:
  --sections N [N ...]  Run specific section numbers (default: all 40)
  --skip-fraud          Skip fraud detection sections 33-40
  --sample              Use sample.csv instead of full dataset
  --csv CSV             Path to a specific CSV file to analyse
```

### Examples

```bash
# Full pipeline
uv run main.py

# Only EDA sections
uv run main.py --sections 1 2 3 4 5

# Quick test with sample data
uv run main.py --sample --sections 1 5 32

# Everything except fraud
uv run main.py --skip-fraud

# Only fraud detection
uv run main.py --sections 33 34 35 36 37 38 39 40
```

## Logging

Logging is configured via `utils/config.py`:

- **Level**: `INFO`
- **Format**: `HH:MM:SS  LEVEL     message`
- **Logger name**: `medicaid`

Each section logs:

- Section banner (`═══ N. Title ═══`)
- Key metrics and summary statistics
- Output file paths (CSV and PNG)
- Timing information

## Output Organization

```
output/
├── 01_eda_summary.csv
├── 02_monthly_trends.csv
├── ...
├── 32_executive_summary.csv
└── fraud/
    ├── 33_upcoding_flagged.csv
    ├── 34_velocity_anomalies.csv
    └── ...

plots/
├── 01_eda_overview.png
├── 02_monthly_dashboard.png
├── ...
├── 32_executive_summary.png
└── fraud/
    ├── 33_upcoding.png
    ├── 34_velocity_anomalies.png
    └── ...
```

## Creating a Sample Dataset

```bash
uv run create_sample.py
```

This creates a ~1% stratified sample at `data/sample.csv` for rapid development and testing.
