# AGENTS.md — `hhs-opendata/medicaid_analysis`

## What this is

Medicaid provider-spending analysis subproject (EDA, fraud, procedures, providers, temporal, stats, plots).

## Layout (verified by direct listing, 2026-08-29)

```
docs/, eda/, fraud/, output/, plots/, procedures/, providers/, stats/, temporal/, tests/, utils/, visualization/, .python-version, README.md, create_sample.py, main.py, pyproject.toml, run_multi_scale.py, uv.lock
```

## Gotchas

- If the tree changed since 2026-08-29, re-verify the listing against disk.
- Data inputs (`data/*.csv`) and `medicaid.db` are git-ignored; the docs and generated `output/`/`plots/` artifacts in this repo are tracked.
