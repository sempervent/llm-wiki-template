# Architecture

Local-first: **Obsidian** over `wiki/` + `raw/`. **`docs/`** is the operator handbook and optional public mirror.

```mermaid
flowchart TB
  subgraph raw [raw]
    inbox[raw/inbox]
    processed[raw/processed]
    assets[raw/assets]
  end
  subgraph wiki [wiki]
    index[wiki/index.md]
    log[wiki/log.md]
    pages[entities concepts topics analyses ...]
  end
  subgraph docs [docs]
    handbook[docs/]
    site[mkdocs site]
  end
  inbox --> processed
  processed --> pages
  pages --> index
  pages --> log
  handbook --> site
```

## Layers

| Layer | Path | Role |
|-------|------|------|
| Evidence | `raw/` | Provenance; no silent edits after filing |
| Synthesis | `wiki/` | Maintained model + routing |
| Handbook | `docs/` | How-to; not the live wiki |

## Hierarchy

1. Obsidian (local repo)
2. `wiki/` + `raw/`
3. `AGENTS.md`
4. GitHub (review)
5. Pages (optional public handbook)

## Operator loop

1. **`wiki/index.md`** → pick cluster
2. Work in `raw/` + `wiki/`
3. Update `wiki/index.md` / hubs
4. Append **`wiki/log.md`**
5. `make validate`

CI runs the same gates as `make check` (see [`validation.md`](operations/validation.md)).

**Next:** [`operations/obsidian.md`](operations/obsidian.md).
