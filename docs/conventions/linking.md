# Linking conventions

## Relative Markdown links

Use standard markdown links with **relative paths** from the current file:

```markdown
[Concept](../../wiki/concepts/llm-wiki-pattern.md)
```

From `docs/…`, cross-link to the vault under `wiki/…` using a repo-relative path as above (GitHub and Obsidian). The MkDocs handbook under `docs/` does not ship `wiki/` pages, so those links are for repository navigation, not the published handbook build.

## Wikilinks

Obsidian wikilinks (`[[...]]`) are optional. If you use them, keep a parallel `.md` relative link for tooling that does not understand wikilinks.

## Graph-friendly structure

- Prefer **descriptive filenames** (`kebab-case.md`).
- Link **upward** to concepts and **sideways** to related entities.
- Avoid orphan pages: link from index or from another page (see validation rules in `AGENTS.md`).
