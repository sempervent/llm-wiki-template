# Ingest checklist

Use this when adding new material to the vault.

- [ ] Raw file placed under `raw/inbox/` or `raw/processed/` per policy
- [ ] Source-note created or updated in `wiki/source-notes/`
- [ ] Relevant entity/concept/topic pages updated
- [ ] `wiki/index.md` lists new or renamed pages
- [ ] `wiki/log.md` appended with `ingest` entry
- [ ] `uv run python scripts/validate_wiki.py` passes (use `--strict` before merge)
