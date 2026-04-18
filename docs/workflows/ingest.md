# Ingest

Add evidence to `raw/`, ground it in **`wiki/source-notes/`**, then **activate** into synthesis (do not leave knowledge trapped in source-notes).

## Steps

1. **Capture** — `raw/inbox/` → stable `raw/processed/...`; never rewrite old processed meaning; add new files instead.
2. **Source-note** — `wiki/source-notes/...` with `source_ids` → raw paths; add Evidence summary for high-leverage sources.
3. **Activate** — update canonical pages, hubs, comparisons, checklists as needed.
4. **Route** — `wiki/index.md` + hubs when navigation changes.
5. **Log + validate** — append `wiki/log.md` (`ingest`); `make validate`.

## PDFs

```bash
uv run python scripts/ingest_pdf.py raw/inbox/your-file.pdf
```

## Done

Stable raw paths; source-note; activation done or deferred; routing current; log appended; validation passes.

Checklist: `templates/ingest-checklist.md`.

**Next:** **`wiki/index.md`**, then `AGENTS.md` § Ingest.
