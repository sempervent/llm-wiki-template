# Page schema

Pages in taxonomy directories use YAML frontmatter with at least `title` and `page_type`.

## Common fields

| Field | Usage |
|-------|--------|
| `title` | Canonical display title |
| `page_type` | `overview`, `source_note`, `entity`, `concept`, `topic`, `analysis`, `comparison`, `timeline`, `glossary`, `operating_doc` |
| `status` | `draft`, `active`, `deprecated` |
| `created` / `updated` | ISO dates |
| `source_ids` | Strings identifying raw paths or stable ids |
| `tags` | Short tokens for search and grouping |
| `confidence` | `low`, `medium`, `high` |
| `review_status` | `unreviewed`, `reviewed`, `stale` |
| `supersedes` / `superseded_by` | Deprecation chains |

Not every field is required on every page type; the validator enforces `title` and `page_type` for structured pages under `wiki/` subtrees (see `scripts/wiki_common.py`).
