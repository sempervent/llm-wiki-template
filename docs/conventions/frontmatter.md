# Frontmatter

Wiki pages may start with YAML frontmatter delimited by `---`:

```markdown
---
title: Example
page_type: concept
status: active
created: 2026-04-17
tags: [demo]
---

# Example
```

## Parser notes

- Use spaces, not tabs, in YAML.
- Lists can be bracketed or indented YAML lists.
- The validator uses PyYAML; keep frontmatter small and deterministic.

## Optional: Dataview-friendly fields (Obsidian)

If you use **[Dataview](https://github.com/blacksmithgu/obsidian-dataview)**, prefer **lists and ISO dates** in frontmatter so queries stay predictable:

| Field | Dataview use |
|-------|----------------|
| `created`, `updated` | Sort/filter with `SORT updated DESC` |
| `tags` | `WHERE contains(tags, "token")` |
| `page_type`, `status`, `review_status` | Table columns and filters |

Example:

```dataview
TABLE title, updated FROM "wiki/concepts"
WHERE page_type = "concept"
SORT updated DESC
```

You may add namespaced custom keys (for example `dv_priority`) as long as YAML stays valid; document anything agents should mirror in this page or in `AGENTS.md`.
