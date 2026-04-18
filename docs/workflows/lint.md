# Lint workflow

**Goal:** Periodic hygiene—links, index coverage, duplicates, orphans—without rewriting history.

## Steps

1. Run `uv run python scripts/validate_wiki.py --strict`.
2. Run `uv run python scripts/rebuild_index.py` and fix any missing index links.
3. Address stale pages (`review_status: stale`) or mark supersession with `superseded_by`.
4. Append `wiki/log.md` with a `lint` entry.
5. Commit small, scoped changes.

## Done definition

Validator strict clean; index audit clean; log documents the pass.

See [`templates/lint-checklist.md`](https://github.com/sempervent/llm-wiki-template/blob/main/templates/lint-checklist.md) (local path: `templates/lint-checklist.md`).
