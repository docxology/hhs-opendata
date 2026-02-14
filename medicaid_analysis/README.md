# Medicaid Provider Spending — Analysis Pipeline

Modular 40-section analysis of CMS Medicaid provider-level spending data. Organized into 8 subpackages covering EDA, statistical modeling, provider behavior, procedure analysis, temporal trends, visualization, and fraud detection.

## Quick Start

```bash
# Full analysis (all 40 sections)
uv run main.py

# Specific sections only
uv run main.py --sections 1 2 5 32

# Skip fraud detection (sections 33-40)
uv run main.py --skip-fraud

# Use sample dataset
uv run main.py --sample
```

## Architecture

```
medicaid_analysis/
├── main.py                 # Pipeline orchestrator (CLI)
├── utils/                  # Shared config, formatting, I/O, DB
├── eda/                    # Exploratory data analysis (S01-S05, S12)
├── stats/                  # Statistical tests & models (S06, S08-S09, S15, S17-S18, S31)
├── providers/              # Provider behavior analysis (S07, S10, S13, S16, S24, S27, S29)
├── procedures/             # HCPCS / procedure analysis (S14, S23, S26, S30)
├── temporal/               # Time-series & seasonality (S11, S19, S21-S22, S25)
├── visualization/          # Deep-dive charts & dashboards (S20, S28, S32)
├── fraud/                  # Fraud detection suite (S33-S40)
├── docs/                   # Comprehensive documentation
├── output/                 # Generated CSVs
└── plots/                  # Generated visualizations
```

## Data

Source: [CMS Medicaid State Drug Utilization Data](https://data.cms.gov/)  
File: `data/medicaid-provider-spending.csv`  
Records: ~227 million rows, covering 617K+ billing providers and 10.8K+ HCPCS codes.

## Documentation

See [`docs/`](docs/) for:

- [Architecture Guide](docs/architecture.md)
- [Module Reference](docs/modules.md)
- [Section Catalog](docs/sections.md)
- [Fraud Detection Guide](docs/fraud_guide.md)
- [Data Dictionary](docs/data_dictionary.md)
- [Configuration](docs/configuration.md)
- [Contributing](docs/contributing.md)

## Dependencies

Managed with [uv](https://docs.astral.sh/uv/):

- `pandas`, `numpy` — data manipulation
- `matplotlib`, `seaborn` — visualization
- `duckdb` — SQL-based analytics engine
- `scipy` — statistical tests
- `scikit-learn` — clustering (fraud module)
