# Raw layer

Immutable (after processing) source material: imports, excerpts, OCR dumps, and referenced files.

- **`inbox/`** — Drop new sources here before filing to `processed/`. For PDFs, run `scripts/ingest_pdf.py` to emit markdown under `processed/<year>/` (see `docs/workflows/ingest.md`).
- **`processed/`** — Stable, read-only archive paths referenced by `wiki/source-notes/`.
- **`assets/`** — Binary attachments (PDFs, images) referenced from raw notes or wiki.

Agents **do not edit** `processed/` contents to “fix” meaning. Errata belong in new raw notes or in the wiki synthesis layer with clear attribution.

See `docs/workflows/ingest.md`.
