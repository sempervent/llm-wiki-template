# Lint

Keep structure valid and navigation healthy—not only “script passes.”

## Steps

1. `make validate`
2. `uv run python scripts/rebuild_index.py` — fix index + hub links
3. Review `review_status: stale`, contradictions, `scripts/wiki_wikilinks.py` as needed
4. Append `wiki/log.md` (`lint`)
5. Small commits

## Done

Strict validator clean; index/hubs match pages; stale/orphan issues fixed or deferred in log.

Checklist: `templates/lint-checklist.md`.

**Next:** **`wiki/index.md`**, then `make check` before merge.
