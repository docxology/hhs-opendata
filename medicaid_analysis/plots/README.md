# `plots/`

Generated PNG figures from the 40-section pipeline (`uv run main.py`, run from `medicaid_analysis/`). **Regenerable**. Mirrors the `output/` per-sample-fraction layout: `1pct/`-`100pct/` written by `run_multi_scale.py` via `MEDICAID_PLOTS_DIR`, each with a `fraud/` subfolder; top-level `NN_*.png` and `fraud/` are from the most recent default-output run. Naming: `NN_section_slug.png` matching section numbers in `../README.md`.

Mirrors: `../output/` follows the same per-scale layout.

Part of the medicaid_analysis subproject (generated artifacts; local-only, never committed). Parent: `../README.md`.
