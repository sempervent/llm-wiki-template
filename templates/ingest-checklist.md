# Ingest checklist

Use this for every meaningful ingest batch.

- [ ] Raw file captured under `raw/inbox/` and filed to stable `raw/processed/...` path (optional: `scripts/ingest_pandoc.py` for DOCX/PPTX/PDF+images; `scripts/ingest_pdf.py` for PDF text-only)
- [ ] Source-note created/updated in `wiki/source-notes/` with correct `source_ids`
- [ ] Activation decision made (canonical page/hub/comparison/checklist update OR explicit deferral)
- [ ] Relevant synthesis pages updated (not source-note only when activation is needed)
- [ ] Routing surfaces updated (`wiki/index.md`, topic hubs, canonical cross-links)
- [ ] `wiki/log.md` appended with `ingest` entry
- [ ] `make validate` passes (or `just validate`)
