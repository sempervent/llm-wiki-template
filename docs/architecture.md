# Architecture

```mermaid
flowchart TB
  subgraph raw [raw layer immutable evidence]
    inbox[raw/inbox]
    processed[raw/processed]
    assets[raw/assets]
  end
  subgraph wiki [wiki layer agent maintained]
    index[wiki/index.md]
    log[wiki/log.md]
    pages[entities concepts analyses ...]
  end
  subgraph handbook [docs layer operator docs]
    mk[MkDocs site]
  end
  inbox --> processed
  processed --> pages
  pages --> index
  pages --> log
  handbook --> mk
```

## Layers

| Layer | Path | Role |
|-------|------|------|
| **Raw** | `raw/` | Immutable sources after filing; provenance for claims |
| **Wiki** | `wiki/` | Structured synthesis: taxonomy, links, analyses |
| **Handbook** | `docs/` | How to run the system; built by MkDocs |
| **Examples** | `examples/` | Isolated demos; not the live corpus unless promoted |

## Contracts

- **`AGENTS.md`** — highest-priority rules for agents (ingest/query/lint, log append-only, no raw edits).
- **`wiki/index.md`** — human/agent navigation catalog.
- **`wiki/log.md`** — append-only history with parseable headings.

## Tooling

Python scripts under `scripts/` enforce deterministic checks. CI runs `uv sync --frozen`, then `validate_wiki.py --strict`, `pytest`, and `mkdocs build --strict` via `uv run`.
