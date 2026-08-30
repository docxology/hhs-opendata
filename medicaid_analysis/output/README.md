# `output/`

Generated analysis artifacts from the 40-section pipeline (`uv run main.py`, run from `medicaid_analysis/`). **Regenerable** — delete and re-run the pipeline to recreate; nothing here is hand-authored. `1pct/`-`100pct/` hold per-sample-fraction runs (written by `run_multi_scale.py` via the `MEDICAID_OUTPUT_DIR`/`MEDICAID_PLOTS_DIR` env vars), each with its own `fraud/` subfolder; the top-level `NN_*.csv` files and `fraud/` are from the most recent default-output run. Naming: `NN_section_slug.csv` matching the section numbers in `../README.md`.

Mirrors: `../plots/` follows the same per-scale layout.

Part of the medicaid_analysis subproject (generated artifacts; local-only, never committed). Parent: `../README.md`.
