# LLM Wiki Template

**Primary interface:** open this repo in **Obsidian** (vault = repo root or `wiki/`). **Primary corpus:** `wiki/` + `raw/`. **Primary law:** [`AGENTS.md`](AGENTS.md).

## First 10 minutes

```bash
git clone https://github.com/YOUR_USER/YOUR_REPO.git
cd YOUR_REPO
uv sync --all-groups
```

1. Obsidian → open **`wiki/index.md`**
2. Open **`AGENTS.md`**
3. Edit any `wiki/` page (e.g. `wiki/concepts/llm-wiki-pattern.md`)
4. `make validate`

## Daily loop

| Step | Where |
|------|--------|
| Capture | `raw/` |
| Ground | `wiki/source-notes/` |
| Activate | canonical pages / hubs / comparisons (not source-note only) |
| Route | `wiki/index.md` + topic hubs |
| Record | `wiki/log.md` (append-only) |
| Check | `make validate` before commit |

## Layout

| Path | Role |
|------|------|
| `AGENTS.md` | Operating contract |
| `wiki/` | Synthesis |
| `raw/` | Immutable evidence |
| `docs/` | Handbook (optional public mirror via Pages) |
| `scripts/`, `templates/`, `examples/` | Tooling, scaffolds, specimens |

## Commands

`just` mirrors `make` (same names).

```bash
make sync
make validate
make check      # validate + test + strict docs build
make docs-serve # local handbook only
```

**Next:** [`docs/quickstart.md`](docs/quickstart.md) → then [`docs/operations/obsidian.md`](docs/operations/obsidian.md).

## License

`LICENSE`.
