# hhs-opendata — Agent Guide

## Layout

- `medicaid_analysis/` — the analysis package (CLI `main.py`, sections under
  `eda/`, `stats/`, `providers/`, `procedures/`, `temporal/`,
  `visualization/`, `fraud/`; own `pyproject.toml`, run with `uv`).
- `data/` — raw dataset location (git-ignored; ~11 GB CSV / ~3.4 GB compressed).
- `docs/` — [documentation index](README.md), [pipeline overview](medicaid_analysis.md),
  [analysis guides](analysis/README.md) and the [manuscript sources](manuscript/README.md).
- Root `README.md` — dataset schema, coverage, quick start, technology table.

## Conventions observed

- Raw CSV and local DuckDB files stay outside Git. The repo tracks selected
  aggregate analysis outputs and publication artifacts.
- Analysis is sectioned and modular; outputs land in `medicaid_analysis/output/`
  and `medicaid_analysis/plots/`.
- `uv sync` + `uv run main.py` inside `medicaid_analysis/` per root README (all 40 sections; `run_multi_scale.py` for per-scale runs).

## How docs here are maintained

- `docs/README.md` indexes the docs tree; `docs/medicaid_analysis.md` describes
  pipeline architecture. Keep section counts and output claims in sync with the
  actual `medicaid_analysis/` tree when it changes.

## Notes for agents

- Do not fabricate dataset statistics; the root README's schema table is the
  reference (source: HHS Open Data "Medicaid Provider Spending").
