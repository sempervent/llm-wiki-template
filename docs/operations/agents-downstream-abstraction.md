# AGENTS.md and downstream forks

The repository may include **`AGENTS-smartfarmwiki.md`** in the repo root (see [snapshot on GitHub](https://github.com/sempervent/llm-wiki-template/blob/main/AGENTS-smartfarmwiki.md) when published): a **downstream** fork diff for generic contract improvements. It is **not** the active contract; **[`AGENTS.md`](https://github.com/sempervent/llm-wiki-template/blob/main/AGENTS.md)** always wins locally.

## Abstracted into the template (generic)

- **Ingest = capture + activation** — filing raw/source-notes is necessary but not always sufficient; agents route knowledge into canonical pages, hubs, and structured artifacts.
- **Evidence summary guidance** — optional structured fields for high-leverage source-notes (abstract, authority, decision relevance, links, claims, open questions).
- **Artifact choice** — when matrices, comparisons, standards, guides, and checklists are appropriate; prefer extending existing surfaces.
- **Structural vs integration quality** — CI validates structure; **integration** (activation, hub updates) is policy tracked via log and review.
- **Structured derivative artifacts** — prefer tables, checklists, norms, and routing pages when they beat narrative-only notes.
- **Evidence routing** — after material ingests, update index, overview, hubs, or canonical pages so readers can find the work.
- **Canonicalization** — search for a home before adding overlapping pages; link upward from supporting notes.
- **Hubs and ownership language** — canonical pages own subject clusters; topic hubs and `index.md` are routing contracts.
- **Sensitive raw / claim strength / entity-first** — shortened, domain-neutral versions of downstream policy.

## Intentionally omitted (domain- or fork-specific)

- **Business-plan packages**, **site-intelligence**, and **named geography** patterns.
- **Package strategy** wiki pages and **procedural guide** packaging specific to one product domain.
- **`page_subtype` / `operational_maturity`** full specification — mentioned only as an optional fork extension; the template validator does not require them.
- **Fork-only scripts** (e.g. `pdf_to_markdown` vs `ingest_pdf`, `validate_raw_pdf_links`) — template keeps its own script set in `AGENTS.md`.
- **MkDocs publishing from `wiki/` only** — the template publishes **`docs/`** via MkDocs; forks may reconfigure.
- **Mission-and-values** wiki page pointers and **farm / agritourism** examples.
- **Detailed regulatory** lists — replaced with a short **high-stakes claims** rule (safety, compliance, health, legal).

When porting a fork forward, merge **behavior** here and keep **domain prose** in `wiki/overview.md` and concepts—not in `AGENTS.md`.
