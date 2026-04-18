# Agent maintenance

Agents should traverse **`wiki/index.md`** first, then only pages in scope.

## Session loop

1. `wiki/index.md` → relevant cluster
2. Read `raw/` only when provenance matters
3. Update synthesis + routing (`wiki/index.md`, hubs)
4. Append `wiki/log.md`
5. `make check` before PR (or `make validate` for wiki-only edits)

## Quality

- **Duplicates:** merge or link; prefer one canonical page
- **Hubs:** topic pages aggregate siblings; avoid orphan-only navigation
- **Evidence:** cite `raw/` paths in wiki text or `source_ids`

## Logging

Append-only `wiki/log.md` with correct headings (`ingest`, `query`, `lint`, …).

## PRs

Small diffs; cite `wiki/` paths in the PR body.

**Next:** open **`wiki/index.md`** in Obsidian, or **`AGENTS.md`** for full contract.
