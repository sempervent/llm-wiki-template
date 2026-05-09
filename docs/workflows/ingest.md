# Ingest

Add evidence to `raw/`, ground it in **`wiki/source-notes/`**, then **activate** into synthesis (do not leave knowledge trapped in source-notes).

## Steps

1. **Capture** — `raw/inbox/` → stable `raw/processed/...`; never rewrite old processed meaning; add new files instead.
2. **Source-note** — `wiki/source-notes/...` with `source_ids` → raw paths; add Evidence summary for high-leverage sources.
3. **Activate** — update canonical pages, hubs, comparisons, checklists as needed.
4. **Route** — `wiki/index.md` + hubs when navigation changes.
5. **Log + validate** — append `wiki/log.md` (`ingest`); `make validate`.

## PDF (text only)

Fast path when you only need page text (no figure extraction):

```bash
uv run python scripts/ingest_pdf.py raw/inbox/your-file.pdf
```

## PDF, Word, PowerPoint → Markdown + images (Obsidian)

Use **Pandoc** when you want Markdown **and** embedded images on disk next to the note (Obsidian shows them via relative paths).

**Install** `pandoc` on your machine (not a Python package). PDF conversion usually also needs **Poppler** (e.g. `brew install pandoc poppler` on macOS; `apt install pandoc poppler-utils` on Debian/Ubuntu).

```bash
uv run python scripts/ingest_pandoc.py raw/inbox/report.docx
uv run python scripts/ingest_pandoc.py raw/inbox/slides.pptx
uv run python scripts/ingest_pandoc.py raw/inbox/scan.pdf
```

Output:

- `raw/processed/<year>/<slug>.md` — YAML frontmatter + title + body
- `raw/processed/<year>/<slug>_media/` — images (`…/media/…` by Pandoc convention)

Open the `.md` in Obsidian from a vault rooted at the repo (or `wiki/` — prefer repo root so `raw/` paths resolve like the rest of the corpus).

If Pandoc fails on PDF, use `ingest_pdf.py` for text-only extraction, or fix Poppler/Pandoc and retry.

## Done

Stable raw paths; source-note; activation done or deferred; routing current; log appended; validation passes.

Checklist: `templates/ingest-checklist.md`.

**Next:** **`wiki/index.md`**, then `AGENTS.md` § Ingest.
