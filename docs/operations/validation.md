# Validation

## Wiki and repository

`scripts/validate_wiki.py` performs deterministic checks:

- Required repository files exist
- `wiki/index.md` links cover all wiki pages (except `index.md` and `log.md`)
- `wiki/log.md` headings match `## [YYYY-MM-DD] kind | title`
- Internal markdown links in `wiki/` resolve to existing files
- Frontmatter `title` and `page_type` on schema pages
- Kebab-case filenames (with exceptions for `index.md`, `log.md`, `overview.md`)
- Duplicate titles (heuristic) and orphan pages (warnings)
- Heuristic scan for misleading “mutable raw” language

Run locally:

```bash
uv sync --all-groups
uv run python scripts/validate_wiki.py --strict
```

CI uses `--strict` so warnings fail the build.

## Handbook (`docs/`)

`scripts/validate_docs_links.py` checks **relative** links between files under `docs/` (and targets elsewhere in the repo, such as `wiki/…`, when linked explicitly). Run it after editing the operator handbook:

```bash
uv run python scripts/validate_docs_links.py
```

`make validate` runs both wiki validation and this pass.

## Generated taxonomy page

`docs/reference/page-taxonomy.md` is **generated** from the **Page taxonomy** section in `AGENTS.md` plus the `templates/` listing. Regenerate after changing taxonomy or templates:

```bash
uv run python scripts/render_taxonomy_doc.py
```

CI runs `scripts/render_taxonomy_doc.py --check` so the committed file cannot drift from `AGENTS.md`.

## MkDocs

The handbook uses **MkDocs Material** with `strict: true` in `mkdocs.yml` so warnings fail `mkdocs build --strict` (same as CI).

## Optional helpers

| Script | Role |
|--------|------|
| `scripts/wiki_search.py` | Regex search across `wiki/**/*.md` (stdlib; no index) |
| `scripts/wiki_wikilinks.py` | Unresolved `[[wikilinks]]` ranked by frequency |
| `scripts/intake_inbox.py` | Summarize files in `raw/inbox/` |

See [`AGENTS.md`](https://github.com/sempervent/llm-wiki-template/blob/main/AGENTS.md) for the full script table.
