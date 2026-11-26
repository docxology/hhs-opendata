# AGENTS.md — `hhs-opendata/medicaid_analysis`

## What this is

Medicaid provider-spending analysis subproject (EDA, fraud, procedures, providers, temporal, stats, plots).

## Layout

```
eda/, fraud/, output/, plots/, procedures/, providers/, stats/, temporal/, tests/, utils/, visualization/, .python-version, README.md, create_sample.py, main.py, pyproject.toml, run_multi_scale.py, uv.lock
```

## Gotchas

- Consolidated guides are under [`docs/analysis/`](../docs/analysis/).
- Data inputs (`data/*.csv`) and `medicaid.db` are git-ignored; the docs and generated `output/`/`plots/` artifacts in this repo are tracked.
