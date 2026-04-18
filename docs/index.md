# LLM Wiki Template

This site is the **operator handbook** for the template: architecture, workflows, conventions, and publishing. Domain knowledge lives in the `wiki/` directory (Obsidian-friendly markdown), not in these docs.

**Start here**

- [Quickstart](quickstart.md) — template → clone → Obsidian → local docs → GitHub Pages
- [Architecture](architecture.md) — raw vs wiki vs docs layers
- [Agent maintenance](operations/agent-maintenance.md) — how `AGENTS.md` governs automation

**Environment**

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`. Run **`uv sync`** once per clone (or after lock changes), then invoke scripts with **`uv run`** (see [Quickstart](quickstart.md)).

**Scripts**

| Script | Purpose |
|--------|---------|
| `scripts/bootstrap.py` | Create missing directories; optional `site_name` |
| `scripts/validate_wiki.py` | Integrity checks (`--strict` in CI) |
| `scripts/rebuild_index.py` | Audit `wiki/index.md` against files on disk |
| `scripts/append_log.py` | Append a formatted `wiki/log.md` entry |
| `scripts/scaffold_page.py` | New page from `templates/` |

The canonical behavioral contract for agents is [`AGENTS.md`](https://github.com/sempervent/llm-wiki-template/blob/main/AGENTS.md) in the repository root (open the same path in your local clone).
