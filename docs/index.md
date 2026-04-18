# Handbook

Explains **how** to run the repo. **Do not** treat this site as the main workspace—that stays **`wiki/`** + **`raw/`** in Obsidian.

**Next:** open [`quickstart.md`](quickstart.md).

## Read order

1. [`quickstart.md`](quickstart.md) — setup sequence
2. [`architecture.md`](architecture.md) — layers
3. [`operations/obsidian.md`](operations/obsidian.md) — vault settings
4. [`operations/agent-maintenance.md`](operations/agent-maintenance.md) — agents

## Rules (short)

- `wiki/index.md` — catalog; start navigation here.
- `wiki/log.md` — append-only.
- Ingest = capture **+** activation (`AGENTS.md`).
- `raw/processed/` — immutable; fix meaning in `wiki/` or new raw files.

## Commands

```bash
make sync
make validate
make check
```
