# Obsidian (primary UI)

Obsidian is the default way to read and edit **`wiki/`** + **`raw/`**.

## Vault layout

| Mode | Open | Tradeoff |
|------|------|----------|
| **Repo root** (recommended) | Entire clone | One vault; `docs/`, `scripts/` visible |
| **`wiki/` only** | `wiki/` subfolder | Cleaner graph; handbook paths need manual hops |

## Settings (suggested)

| Setting | Value |
|---------|--------|
| Files & links → New link format | Relative path to file |
| Files & links → Detect all file extensions | On |
| Files & links → Use `[[Wikilinks]]` | Optional (keep `.md` portable links too) |

## Links

- **Portable:** e.g. `[Quickstart](../quickstart.md)` from this folder (`.md` relatives, not repo-absolute paths)
- **Wikilinks:** `[[foo]]` — run `uv run python scripts/wiki_wikilinks.py` occasionally; CI can rank unresolved links

## Attachments

Prefer `raw/assets/` (or a documented path). Avoid spaces in filenames.

## Graph

Use as a **hint**, not truth. Prefer `wiki/index.md` + hubs for navigation.

## Pitfalls

- Renames: update inbound links or use `aliases` in frontmatter
- Orphans: fix via links + `wiki/index.md`

**Next:** [`agent-maintenance.md`](agent-maintenance.md), or open **`wiki/index.md`** in Obsidian.
