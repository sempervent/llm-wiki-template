# Query workflow

**Goal:** Answer questions using `wiki/` + `raw/`, and persist durable answers when reuse is likely.

## Steps

1. **Search** the wiki catalog (`wiki/index.md`) and relevant pages.
2. **Cite** raw paths for non-obvious claims.
3. **Optional persistence:** create or update an `analyses/` or `concepts/` page; link related entities.
4. **Append `wiki/log.md`** with a `query` entry pointing to the written page.
5. **Run** `uv run python scripts/validate_wiki.py`.

## Filing answers into the wiki

Short-lived answers can stay in chat; durable answers belong in the wiki with explicit limits and citations. Use frontmatter `confidence` and `review_status` honestly.

## Done definition

Answer references wiki/raw; if persisted, page exists and is linked from index or inbound links; log updated; validator clean.
