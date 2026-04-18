# Validation

Run checks continuously, not only before merge.

## Commands

`just` mirrors `make`.

```bash
make validate   # wiki strict + docs links
make check      # full local CI parity
```

## What `validate` covers

`scripts/validate_wiki.py --strict`: required files, `wiki/` links + index, log headings, frontmatter, filenames, duplicates/orphans, mutability heuristics. Plus `scripts/validate_docs_links.py`.

## Taxonomy doc

```bash
uv run python scripts/render_taxonomy_doc.py
```

CI uses `--check` for drift.

## Helpers

| Script | Role |
|--------|------|
| `scripts/wiki_search.py` | Search `wiki/**/*.md` |
| `scripts/wiki_wikilinks.py` | Unresolved `[[wikilinks]]` |
| `scripts/intake_inbox.py` | Inbox summary |

Policy: `AGENTS.md`.

**Next:** [`../quickstart.md`](../quickstart.md).
