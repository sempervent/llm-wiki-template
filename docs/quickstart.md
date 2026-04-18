# Quickstart

Obsidian-first. **`just`** mirrors **`make`** (same names).

| Step | Action |
|------|--------|
| 1 | **Use this template** on GitHub → new repo |
| 2 | `git clone` → `cd` repo |
| 3 | `uv sync --all-groups` |
| 4 | Obsidian → **Open folder as vault** → repo root (or `wiki/` only — see [Obsidian](operations/obsidian.md)) |
| 5 | Open **`wiki/index.md`** |
| 6 | Open **`AGENTS.md`** |
| 7 | Edit a `wiki/` page or add `raw/inbox/` + `wiki/source-notes/` |
| 8 | `make validate` |
| 9 | (optional) `make docs-serve` — handbook preview only |
| 10 | (optional) GitHub **Settings → Pages → GitHub Actions** → push `main` |

**After step 4, next file:** `wiki/index.md`.

**After step 6, next file:** any page linked from `wiki/index.md`.

## Optional: publish handbook

[`operations/publishing.md`](operations/publishing.md)

**Next:** [`operations/obsidian.md`](operations/obsidian.md) for vault ergonomics.
