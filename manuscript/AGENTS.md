# Manuscript — Agent Guide

## Layout

Standard section stubs (`00_abstract.md`…`99_references.md`), `config.yaml`
(+ `.example`), `preamble.md`, `references.bib`.

## Conventions

- All config values are `TODO-OWNER` placeholders; do not render until filled.
- Numeric claims may only come from `medicaid_analysis/output/` and
  `medicaid_analysis/plots/` artifacts actually present on disk.
- Citations go in `references.bib` after verification against a primary source.

## Maintenance

When the pipeline's section structure changes, update `02_methods.md`
references and `docs/medicaid_analysis.md` together.
