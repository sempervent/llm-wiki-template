# Validation

`scripts/validate_wiki.py` performs deterministic checks:

- Required repository files exist
- `wiki/index.md` links cover all wiki pages (except `index.md` and `log.md`)
- `wiki/log.md` headings match `## [YYYY-MM-DD] kind | title`
- Internal markdown links resolve to existing files
- Frontmatter `title` and `page_type` on schema pages
- Kebab-case filenames (with exceptions for `index.md`, `log.md`, `overview.md`)
- Duplicate titles (heuristic) and orphan pages (warnings)
- Heuristic scan for misleading “mutable raw” language

Run locally:

```bash
uv sync
uv run python scripts/validate_wiki.py --strict
```

CI uses `--strict` so warnings fail the build.
