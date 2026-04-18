# Evolving `AGENTS.md` from downstream forks

**Template maintainers** sometimes fold **generic** behaviors learned in **downstream** wikis (longer-running repos that started from this template or share the same pattern). Those forks are **not** shipped here—no private operating contract is checked in. This page records **what** was abstracted into the template and **what** usually stays fork-specific, so you can port ideas without depending on external files in this repository.

## Abstracted into the template (generic)

- **Ingest = capture + activation** — filing raw/source-notes is necessary but not always sufficient; agents route knowledge into canonical pages, hubs, and structured artifacts.
- **Evidence summary guidance** — optional structured fields for high-leverage source-notes (abstract, authority, decision relevance, links, claims, open questions).
- **Artifact choice** — when matrices, comparisons, standards, guides, and checklists are appropriate; prefer extending existing surfaces.
- **Structural vs integration quality** — CI validates structure; **integration** (activation, hub updates) is policy tracked via log and review.
- **Structured derivative artifacts** — prefer tables, checklists, norms, and routing pages when they beat narrative-only notes.
- **Evidence routing** — after material ingests, update index, overview, hubs, or canonical pages so readers can find the work.
- **Canonicalization** — search for a home before adding overlapping pages; link upward from supporting notes.
- **Hubs and ownership language** — canonical pages own subject clusters; topic hubs and `index.md` are routing contracts.
- **Sensitive raw / claim strength / entity-first** — shortened, domain-neutral patterns for local corpora, epistemics, and recurring named subjects.

## Intentionally omitted (typically fork- or domain-specific)

- **Business-plan or “site package”** layouts, **site-intelligence** pages, and **named geography** patterns.
- **Package strategy** or **procedural packaging** docs tied to one product domain.
- **Full optional frontmatter** extensions (e.g. rich `page_subtype` / maturity fields)—forks may add them; this template’s validator focuses on `title` and `page_type` where required.
- **Alternate script names or extra validators** — the **canonical** script list is whatever appears in root **`AGENTS.md`** for this repo.
- **Different MkDocs roots** (e.g. building from `wiki/` instead of `docs/`) — forks may reconfigure; the template documents **`docs/`** as the handbook.
- **Long mission prose or sector examples** in `AGENTS.md` — keep mission and voice in **`wiki/overview.md`** and concepts, not in the contract file.

When porting a fork forward, merge **behavior** into your repo’s **`AGENTS.md`** and keep **domain prose** in the wiki.
