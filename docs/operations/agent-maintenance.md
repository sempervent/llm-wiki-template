# Agent maintenance

Automation (Codex, Claude Code, Cursor agents, etc.) should treat [`AGENTS.md`](https://github.com/sempervent/llm-wiki-template/blob/main/AGENTS.md) as the **highest-priority** contract.

## Priorities

1. `AGENTS.md` — mission, layers, workflows, log rules
2. `README.md` — human orientation
3. Task-specific user instructions

## Session pattern

1. Read `AGENTS.md` and `wiki/index.md`.
2. Perform ingest/query/lint in small, verifiable steps. Ingest is **capture + activation** (see `AGENTS.md`): file evidence, then route it into the wiki model when material warrants it.
3. Run `scripts/validate_wiki.py` before commit.
4. Append `wiki/log.md` for substantive work.

See [Evolving `AGENTS.md` from forks](agents-downstream-abstraction.md) for maintainer-oriented notes (optional).


## Pull requests

- Keep diffs scoped; prefer incremental updates over full rewrites.
- CI must pass: tests, validator, MkDocs strict build.
