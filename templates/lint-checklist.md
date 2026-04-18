# Lint checklist

Periodic maintenance pass.

- [ ] Run `make validate` (or `just validate`)
- [ ] Fix broken internal links
- [ ] Resolve or document orphan pages
- [ ] Review `review_status: stale` pages
- [ ] Reconcile duplicate titles flagged by the validator
- [ ] `uv run python scripts/rebuild_index.py` audit clean
- [ ] Update hub pages when new siblings exist (not index-only)
- [ ] Append `wiki/log.md` with `lint` entry
