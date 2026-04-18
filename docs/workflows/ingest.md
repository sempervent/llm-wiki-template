# Ingest workflow

**Goal:** Add sources to `raw/`, ground them in `wiki/source-notes/`, and update synthesis pages without mutating archived material.

## Steps

1. **Drop or file raw content** under `raw/inbox/`; after triage, move to `raw/processed/...` with stable paths. Do not later rewrite processed text to “fix” meaning—add a new raw note if the source changes.
2. **Create or update a source-note** in `wiki/source-notes/` with frontmatter `page_type: source_note` and `source_ids` pointing at the raw path.
3. **Update entities, concepts, topics, analyses** as needed; add relative cross-links.
4. **Update `wiki/index.md`** so every intentional page is listed.
5. **Append `wiki/log.md`** with an `ingest` entry (`scripts/append_log.py` helps).
6. **Run** `uv run python scripts/validate_wiki.py --strict`.

## Done definition

Raw paths stable; source-notes and synthesis updated; index and log updated; validator clean.

See also: [`templates/ingest-checklist.md`](https://github.com/sempervent/llm-wiki-template/blob/main/templates/ingest-checklist.md) (in your clone: `templates/ingest-checklist.md`).
