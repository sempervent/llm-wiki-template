# Linking conventions

## Relative Markdown links

Use standard markdown links with **relative paths** from the current file:

```markdown
[Concept](../concepts/llm-wiki-pattern.md)
```

This works in GitHub, Obsidian, and MkDocs when pages are included.

## Wikilinks

Obsidian wikilinks (`[[...]]`) are optional. If you use them, keep a parallel `.md` relative link for tooling that does not understand wikilinks.

## Graph-friendly structure

- Prefer **descriptive filenames** (`kebab-case.md`).
- Link **upward** to concepts and **sideways** to related entities.
- Avoid orphan pages: link from index or from another page (see validation rules in `AGENTS.md`).
