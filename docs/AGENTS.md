# hhs-opendata — Agent Guide

## Layout

- `medicaid_analysis/` — the analysis package (CLI `main.py`, sections under
  `eda/`, `stats/`, `providers/`, `procedures/`, `temporal/`,
  `visualization/`, `fraud/`; own `pyproject.toml`, run with `uv`).
- `data/` — raw dataset location (git-ignored; ~11 GB CSV / ~3.4 GB compressed).
- `docs/` — `README.md` (hub) and `medicaid_analysis.md` (pipeline overview:
  40 analysis sections, CSV/plot outputs, stage structure).
- Root `README.md` — dataset schema, coverage, quick start, technology table.

## Conventions observed

- Dataset stays out of git; only code and docs are tracked.
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
