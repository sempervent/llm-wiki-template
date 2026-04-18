---
title: PDF to markdown ingest
page_type: concept
status: active
created: 2026-04-17
updated: 2026-04-17
source_ids:
  - raw/processed/2026/pdf-ingest-demo.md
tags:
  - ingest
  - pdf
  - tooling
review_status: reviewed
---

# PDF to markdown ingest

PDFs are **not** edited in place in this template. The supported path is:

1. Drop the PDF under **`raw/inbox/`** (or another path under the repo if you prefer—see the script’s `--help`).
2. Run **`uv run python scripts/ingest_pdf.py <path-to.pdf>`** to write a **new** markdown file under **`raw/processed/<year>/`**. Extraction uses **PyMuPDF** (`fitz`): plain text per page, grouped under `## Page N` headings.
3. Add or update **`wiki/source-notes/`**, synthesis pages, **`wiki/index.md`**, and append **`wiki/log.md`**; run **`uv run python scripts/validate_wiki.py --strict`**.

**Limits**

- Output is **text extraction**, not layout-perfect reconstruction; complex tables and two-column PDFs may need manual cleanup or a different tool chain.
- Do not rewrite **`raw/processed/`** to “fix” extraction errors—file a new raw note or wiki errata instead.

**Example**

- Source-note [`pdf-ingest-demo`](../source-notes/pdf-ingest-demo.md) and handbook steps in [`docs/workflows/ingest.md`](../../docs/workflows/ingest.md).
