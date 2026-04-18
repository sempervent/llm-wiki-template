# Ingest workflow

**Goal:** Add sources to `raw/`, ground them in `wiki/source-notes/`, and update synthesis pages without mutating archived material.

## Steps

1. **Drop or file raw content** under `raw/inbox/`; after triage, move to `raw/processed/...` with stable paths. Do not later rewrite processed text to “fix” meaning—add a new raw note if the source changes. **`AGENTS.md`** treats ingest as **capture + activation**: after grounding a source-note, decide whether to route findings into canonical pages, hubs, comparisons, or other structured artifacts—not only the source-note.

   **PDFs:** For **PDF** sources, generate a new processed markdown file with text extraction (does not replace manual review for complex layouts):

   ```bash
   uv sync   # runtime deps include PyMuPDF; use `uv sync --all-groups` for docs/dev tools too
   uv run python scripts/ingest_pdf.py raw/inbox/your-file.pdf
   ```

   Optional flags: `--slug my-file`, `--title "Human title"`, `--year 2026`, `--ingested YYYY-MM-DD`, `--dry-run`. The script writes under `raw/processed/<year>/<slug>.md` and refuses to overwrite unless you pass `--force`. Keep the original PDF under `raw/inbox/` or `raw/assets/` as you prefer; cite both in the source-note if both exist.

2. **Create or update a source-note** in `wiki/source-notes/` with frontmatter `page_type: source_note` and `source_ids` pointing at the raw path.
3. **Update entities, concepts, topics, analyses** as needed; add relative cross-links.
4. **Update `wiki/index.md`** so every intentional page is listed.
5. **Append `wiki/log.md`** with an `ingest` entry (`scripts/append_log.py` helps).
6. **Run** `uv run python scripts/validate_wiki.py --strict`.

## Done definition

Raw paths stable; source-notes and synthesis updated; index and log updated; validator clean.

See also: [`templates/ingest-checklist.md`](https://github.com/sempervent/llm-wiki-template/blob/main/templates/ingest-checklist.md) (in your clone: `templates/ingest-checklist.md`).
