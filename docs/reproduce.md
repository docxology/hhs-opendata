# Reproduce the archived result

This replay reads the archived exploratory summary, yearly table,
and annual spending figure. It verifies their Git blobs and SHA-256
digests, compares the annual totals with the archived overall record,
and stages a small output evidence file. The retained snapshot is
`317c24bbdd823a89a85853982919b3735bcaaefd`. If a shallow checkout
omits it, fetch that public commit first.

For the full analytical workflow and raw input requirements, see the
[analysis guide](medicaid_analysis.md). The publication replay uses
the checked-in aggregate outputs.

From the repository root, use a dedicated
[Docxology Template checkout](https://github.com/docxology/template)
with Pandoc, pandoc-crossref, and XeLaTeX installed:

```bash
template_dir=/absolute/path/to/template
git -C "$template_dir" switch --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
mkdir -p "$template_dir/projects/working"
git worktree add --no-checkout --detach "$template_dir/projects/working/hhs-opendata" HEAD
git -C "$template_dir/projects/working/hhs-opendata" sparse-checkout set --cone docs
git -C "$template_dir/projects/working/hhs-opendata" checkout --detach HEAD
python3 "$template_dir/projects/working/hhs-opendata/docs/replay_archive.py"
cd "$template_dir"
uv sync --locked --python 3.14 --no-dev
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/hhs-opendata
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/hhs-opendata
```

Look under `projects/working/hhs-opendata/output/` for the PDF, web
document, source evidence summary, and validation reports.
