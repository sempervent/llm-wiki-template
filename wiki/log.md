# Wiki log

Append-only chronological record. New entries go at the **bottom**. Heading format is validated by `scripts/validate_wiki.py`.

---

## [2026-04-17] policy | Initialize template wiki

- Seeded `wiki/` with example pages demonstrating taxonomy and linking.
- Established `raw/processed/2026/example-llm-wiki-note.md` as immutable demo source.
- Documented conventions in `AGENTS.md` and `docs/`.

---

## [2026-04-17] ingest | Example LLM Wiki note

- Filed demo raw source at `raw/processed/2026/example-llm-wiki-note.md`.
- Added source-note [`source-notes/example-llm-wiki-note.md`](source-notes/example-llm-wiki-note.md) and linked from [`concepts/llm-wiki-pattern.md`](concepts/llm-wiki-pattern.md).

---

## [2026-04-17] query | What is the LLM Wiki pattern?

- Answer captured in [`analyses/why-synthesis-layer.md`](analyses/why-synthesis-layer.md) with pointers to concepts and comparisons.

---

## [2026-04-17] lint | Template validation pass

- Ran `validate_wiki.py` with `--strict`; fixed index and link set for demo pages.
---

## [2026-04-17] ingest | PDF to markdown ingest

- Added `scripts/ingest_pdf.py` (PyMuPDF) and `pymupdf` dependency; documented in `docs/workflows/ingest.md` and `README.md`.
- Demo: `raw/inbox/pdf-ingest-demo.pdf` → `raw/processed/2026/pdf-ingest-demo.md`.
- New wiki pages: `concepts/pdf-to-markdown-ingest.md`, `source-notes/pdf-ingest-demo.md`; updated `index.md` and `concepts/llm-wiki-pattern.md`.
---

## [2026-04-18] policy | Dev UX: dependency groups, Makefile, docs validation, optional pre-commit

- Split **runtime** vs **docs** vs **dev** dependencies in `pyproject.toml`; CI uses `uv sync --frozen --all-groups`.
- Added `Makefile` targets (`validate`, `test`, `docs-serve`, `docs-build`, `bootstrap`, taxonomy render/check).
- Added `scripts/validate_docs_links.py`, `mkdocs.yml` `strict: true`, generated `docs/reference/page-taxonomy.md` via `scripts/render_taxonomy_doc.py`.
- Optional scripts: `wiki_search.py`, `wiki_wikilinks.py`, `intake_inbox.py`; `.pre-commit-config.yaml` + dev dependency `pre-commit`.
- Extended `AGENTS.md` (query workflow example, example lint policy) and handbook pages (`docs/operations/validation.md`, Dataview notes in frontmatter conventions).
---

## [2026-04-18] policy | Add justfile mirroring Makefile

- Added `justfile` with recipes matching `Makefile` (`just validate`, `just docs-serve`, etc.); documented in `README.md` and handbook index/quickstart.
---

## [2026-04-18] policy | AGENTS: ingest activation + routing (downstream abstraction)

- Revised `AGENTS.md` with capture+activation ingest, evidence-summary guidance, artifact table, structural vs integration quality, canonicalization, hubs, derivative artifacts, evidence routing, and generic claim/entity/sensitive-raw rules.
- Added `docs/operations/agents-downstream-abstraction.md`; linked from agent-maintenance and ingest workflow; regenerated `docs/reference/page-taxonomy.md`.
---

## [2026-04-18] refactor | Remove downstream AGENTS snapshot from template

- Deleted `AGENTS-smartfarmwiki.md` (private/downstream reference); template stays self-contained.
- Rewrote `docs/operations/agents-downstream-abstraction.md` as maintainer guidance only—no local fork artifact required; updated `agent-maintenance.md` link text.
---

## [2026-04-18] policy | Template neutrality: fork abstraction wording

- Tightened `docs/operations/agents-downstream-abstraction.md` “omitted” list to remove sector-specific jargon; kept the same intent in generic language.
- `AGENTS.md` entity-first rule: “sites” → “locations” for neutral reading.

