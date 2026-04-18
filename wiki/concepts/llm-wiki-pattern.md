---
title: LLM Wiki pattern
page_type: concept
status: active
created: 2026-04-17
updated: 2026-04-17
source_ids:
  - raw/processed/2026/example-llm-wiki-note.md
tags:
  - architecture
  - methodology
review_status: reviewed
---

# LLM Wiki pattern

The **LLM Wiki** pattern separates **immutable raw sources** from a **maintained markdown wiki** that agents update over time. The wiki is not a dump: it is structured synthesis with stable paths, taxonomy, and an append-only log.

**Core invariants**

1. **Raw** — append-only evidence; corrections happen via new files or wiki-level errata.
2. **Wiki** — compounding model: entities, concepts, analyses, with citations back to raw.
3. **Operations** — `index.md` for navigation, `log.md` for history, validators for integrity.

**Source grounding**

- See source-note [`example-llm-wiki-note`](../source-notes/example-llm-wiki-note.md) for the demo raw excerpt.
- For PDFs, see [`PDF to markdown ingest`](pdf-to-markdown-ingest.md) and the [`pdf-ingest-demo`](../source-notes/pdf-ingest-demo.md) source-note.
