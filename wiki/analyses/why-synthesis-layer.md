---
title: Why a synthesis layer
page_type: analysis
status: active
created: 2026-04-17
updated: 2026-04-17
source_count: 1
source_ids:
  - raw/processed/2026/example-llm-wiki-note.md
tags:
  - analysis
  - architecture
confidence: medium
review_status: reviewed
---

# Why a synthesis layer

**Question:** Why maintain a wiki instead of only storing notes in `raw/`?

**Answer (durable):**

Raw captures **what was said** in sources; the wiki captures **how ideas connect**—entities, timelines, comparisons—without mutating evidence. That separation keeps provenance intact while allowing the model to improve structure over time.

**Evidence**

- Demo raw excerpt: [`raw/processed/2026/example-llm-wiki-note.md`](../../raw/processed/2026/example-llm-wiki-note.md)
- Conceptual framing: [`LLM Wiki pattern`](../concepts/llm-wiki-pattern.md)
- Comparison: [`Raw vs wiki`](../comparisons/raw-vs-wiki.md)

**Limits**

- This page is template demo content; replace with domain-specific analyses in a real vault.
