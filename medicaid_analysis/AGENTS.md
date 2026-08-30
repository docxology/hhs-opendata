# AGENTS.md — `hhs-opendata/medicaid_analysis`

> Local-only path under `projects/ongoing/DataTools/` — matched by the
> root `.gitignore` rule `projects/*`; never commit. Repo-wide policy:
> see `/Volumes/external_drive/Git/template/projects/ongoing/AGENTS.md`.

## What this is

Medicaid provider-spending analysis subproject (EDA, fraud, procedures, providers, temporal, stats, plots).

## Layout (verified by direct listing, 2026-08-29)

```
docs/, eda/, fraud/, output/, plots/, procedures/, providers/, stats/, temporal/, tests/, utils/, visualization/, .python-version, README.md, create_sample.py, main.py, pyproject.toml, run_multi_scale.py, uv.lock
```

## Gotchas

- If the tree changed since 2026-08-29, re-verify the listing against disk.
- Never `git add` anything under `projects/ongoing/` (this repo tracks these
  docs explicitly; data and generated artifacts stay untracked).
