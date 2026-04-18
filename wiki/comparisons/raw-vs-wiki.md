---
title: Raw vs wiki
page_type: comparison
status: active
created: 2026-04-17
updated: 2026-04-17
tags:
  - comparison
  - architecture
review_status: reviewed
---

# Raw vs wiki

| Dimension | `raw/` | `wiki/` |
|-----------|--------|---------|
| Purpose | Immutable evidence and captures | Maintained synthesis and navigation |
| Edits after filing | Avoid; add new raw if needed | Expected; incremental |
| Best for | Quotes, imports, attachments | Models, timelines, arguments |
| Failure mode if misused | Silent edits erase provenance | Unsourced claims without `source_ids` |

**See also:** [`LLM Wiki pattern`](../concepts/llm-wiki-pattern.md), [`Synthesis layer`](../glossary/synthesis-layer.md).
