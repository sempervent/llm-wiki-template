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
