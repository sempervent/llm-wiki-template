# Lint checklist

Periodic maintenance pass.

- [ ] Run `uv run python scripts/validate_wiki.py --strict`
- [ ] Fix broken internal links
- [ ] Resolve or document orphan pages
- [ ] Review `review_status: stale` pages
- [ ] Reconcile duplicate titles flagged by the validator
- [ ] `uv run python scripts/rebuild_index.py` audit clean
- [ ] Append `wiki/log.md` with `lint` entry
