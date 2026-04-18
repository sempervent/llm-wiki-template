# AGENTS.md — Operating contract

This file is the **highest-priority behavioral contract** for any automated or human agent working in this repository. When instructions conflict, **follow this document first**, then `README.md`, then task-specific prompts.

---

## Mission

This repository implements an **LLM-maintained markdown wiki**: a persistent, compounding knowledge base where:

- **`raw/`** holds **immutable** source material (notes, imports, excerpts, files).
- **`wiki/`** holds the **agent-authored synthesis** (entities, concepts, analyses, cross-links, and optional structured artifacts such as comparisons or checklists).
- **`docs/`** holds the **published handbook** for humans and agents (MkDocs); it explains *how* the system works, not the domain knowledge itself.

**Separation of concerns:** Keep **behavioral law** here (rules agents load every session). Keep **domain purpose, audience, and voice** in the wiki—typically `wiki/overview.md` and relevant **concept** pages—so they version with synthesis and do not bloat this contract.

The goal is **deterministic, inspectable, markdown-first** workflows: plain files, clear paths, validation scripts, and reproducible doc builds.

---

## Layer definitions

| Layer | Purpose | Mutable by agent? |
|-------|---------|-------------------|
| `raw/` | Provenance-grounded sources; inbox → processed pipeline | **Append / file new sources only. Never edit processed or alter meaning of stored sources.** |
| `wiki/` | Structured knowledge pages, index, log | **Yes**, following rules below |
| `docs/` | Template handbook, architecture, workflows (MkDocs) | **Yes**, when improving operator documentation |
| `scripts/` | Validation and scaffolding | **Yes**, with tests and clear CLI contracts |
| `examples/` | Small worked examples (isolated from production paths) | **Yes**, keep realistic but minimal |

**Do not** treat `examples/` as the live wiki unless the user explicitly asks to promote content.

---

## File ownership model

- **Human or policy owner**: `AGENTS.md`, licensing, and high-level conventions. Agents may propose edits via PRs or patches; destructive convention changes require explicit intent.
- **Agent maintainer**: `wiki/**/*.md` (except obey immutability rules for any symlinked content), `wiki/index.md`, `wiki/log.md`.
- **Build / CI**: `.github/workflows/*`, `mkdocs.yml`, `pyproject.toml`, `uv.lock`.
- **Raw corpus**: files under `raw/processed/` are **write-once** after processing; `raw/inbox/` accepts new drops.

**Canonical pages and hubs:** A **canonical page** is the preferred home for a durable subject cluster (concept, architecture slice, recurring decision). **Topic hubs** (`topics/`) and **`wiki/index.md`** are **routing surfaces**—when you add siblings, update tables or sections so new work is discoverable without relying on search alone.

---

## Mandatory workflows

### Ingest

**1. Capture (evidence on file)**

- Add or confirm raw material under `raw/inbox/` (or processed pipeline per `docs/workflows/ingest.md`).
- Create or update **`source-notes`** in `wiki/source-notes/` pointing to stable `raw/` paths.

**2. Activate (route knowledge into the model)**

Ingestion is **capture + activation**. Filing a source-note alone is not always sufficient.

For each meaningful ingest, explicitly decide whether to:

- leave **source-note only** (capture-first; schedule activation later),
- update a **canonical** synthesis page,
- update a **comparison**, **matrix**, or **topic hub**,
- add or refresh a **guide**, **standard**, or **checklist** (as sections or pages, per taxonomy),
- add a **new** durable page when no canonical home exists yet, or
- **defer** with a short note in **`wiki/log.md`** (and optional `review_status` on the source-note).

If the source affects repeated decisions, risk, architecture, or cross-cutting structure, prefer **routing** into canonical pages or structured artifacts rather than leaving knowledge **only** in `source-notes/`.

**3. Source-note depth for high-value captures**

For **high-leverage** sources (long reports, authoritative references, material that will drive decisions), enrich the source-note with a short **Evidence summary** when useful—**not** required for every trivial drop. Suggested elements (adapt to the source):

- **Abstract** — what the source is and why it matters
- **Authority / modality** — primary vs secondary, data vs opinion
- **Decision relevance** — what decisions this informs
- **Links** — pointers to canonical wiki pages the source supports or constrains
- **Durable claims** — stable takeaways (with confidence)
- **Open questions** — what remains unresolved

Low-volume or placeholder captures may remain **capture-only** until activated; log significant deferrals when material.

**4. When to add matrices, guides, standards, or checklists**

| Artifact | Prefer when |
|----------|----------------|
| **Matrix / comparison** | Readers need **A vs B** or many options in one view; **extend** an existing comparison before adding an overlapping sibling. |
| **Standard** | A short **norm** (“must be true”) with verifiable gates; link to longer guides for sequences. |
| **Guide** | Ordered **steps** or a **doctrine spine** with clear routing to child pages. |
| **Checklist** | **Repeatable** verification; often a **section** inside a standard or guide before warranting a new page. |

**5. Structural validation vs integration quality**

- **Structural (CI):** `scripts/validate_wiki.py --strict` — required files, index coverage, resolvable links, log headings, frontmatter on schema pages, kebab-case, duplicate titles / orphans (heuristic).
- **Integration (policy):** activation completed where promised, hubs and canonical pages updated so evidence is not **trapped** in source-notes. A clean CI pass **without** routing can still be **integration debt**—record significant gaps in `wiki/log.md` when you defer.

**6. Update synthesis and record**

- Update relevant entity/concept/topic pages; add cross-links.
- **Append** `wiki/log.md` with an `ingest` entry (see Log format).
- **Update** `wiki/index.md` if new pages were added or titles changed.
- Run `uv run python scripts/validate_wiki.py` before commit.

### Query

1. Answer from `wiki/` + cited `raw/` paths; do not invent provenance.
2. If the answer should persist, **create or update** a durable wiki page (often `analyses/` or `concepts/`) and link it from `index.md` when appropriate.
3. **Append** `wiki/log.md` with `query` entry summarizing the question and where the answer lives.

### When answering a question, read index.md first, then traverse only relevant pages, then cite the pages used, and optionally file the answer back into the wiki if it creates durable value.

1. Open **`wiki/index.md`** first; use it to choose clusters and only open pages needed for the question.
2. Traverse **relevant** pages (and cited `raw/` when provenance matters), not the whole vault by default.
3. **Cite** the wiki paths (and raw paths) your answer depended on.
4. If the result has durable reuse value, **file it** into `wiki/` (often `analyses/` or `concepts/`), update `wiki/index.md` when appropriate, and append **`wiki/log.md`** with a `query` entry pointing at the new or updated page.

### Lint

Periodic hygiene: link integrity, orphan reduction, stale-claim review, duplicate title checks, index alignment.

1. Run `uv run python scripts/validate_wiki.py` (use `--strict` in CI).
2. Fix or ticket broken links; add missing index entries for intentional pages.
3. **Append** `wiki/log.md` with `lint` entry.

### Example lint policy

Use the validator as the baseline; these are **optional** deeper passes for humans or scheduled jobs:

- **Detect stale claims:** search for `review_status: stale`, old `updated` dates, or sections explicitly marked for review; prefer dated subsections, `supersedes` / `superseded_by`, or new analysis pages over silent edits.
- **Flag contradictions:** when two pages assert incompatible facts, surface the tension (dated evidence, confidence) or split into a new analysis with links—do not silently overwrite.
- **Flag missing backlinks:** beyond orphan detection (no index + no inbound links), watch for **high-value pages** that peers *should* link but do not; add cross-links or an explicit index entry.
- **Flag frequent mentions of missing pages:** run `scripts/wiki_wikilinks.py` for unresolved `[[wikilinks]]` ranked by frequency; prioritize scaffolding missing concept/entity pages or adding `aliases` to existing ones.

---

## Canonicalization before proliferation

- Before adding a **new** analysis or topic page, search **`wiki/index.md`** and the relevant **topic** or **concept** area for an existing **canonical** home.
- **Extend** the canonical page (dated subsection, table row, “See also”) rather than spawning overlapping essays. If overlap is unavoidable, add **`supersedes` / `superseded_by`** (or explicit routing) and log in `wiki/log.md`.
- Supporting pages (pilots, one-off answers) should **link upward** in the opening section; avoid duplicating the canonical page’s outline.

---

## Structured derivative artifacts

When sources improve a **repeatable** decision surface, prefer creating or updating structured artifacts—not only narrative notes:

- comparison tables and matrices
- checklists and gates
- standards (short norms) and procedural guides (longer sequences)
- diagrams or topology descriptions (as markdown + assets)
- decision or routing pages

Do not leave high-value operational knowledge only in source-notes when a structured artifact would serve readers better.

---

## Evidence routing after ingestion

After ingesting important material, ask whether readers can **find and use** the knowledge without relying on search alone. For high-value work, at least one routing surface should usually be updated, for example:

- a **canonical** synthesis page for the subject
- a **topic** hub or comparison that indexes related work
- **`wiki/overview.md`** or **`wiki/index.md`** when navigation or scope shifts

If a strong source-note is not yet linked from a relevant hub or canonical page, **activation** may be incomplete.

---

## Sensitive or local-only raw material

- The **`raw/`** tree may be large, local-only, or partially omitted from clones; CI may not see every file. **Do not** weaken wiki provenance because a path is missing locally—keep stable citations; validate when the full corpus is available.
- Avoid committing **secrets** (passwords, keys, internal hostnames) unless policy explicitly allows; prefer placeholders in published pages and keep sensitive operational detail in approved stores outside the repo when needed.

---

## Claim strength and high-stakes topics

- Prefer **authoritative** sources for upgradeable claims (primary docs, standards, peer-reviewed work, regulator or vendor primary references). Label **anecdotal** or **forum-grade** material honestly.
- Use **`confidence`** and **`review_status`** in frontmatter consistently; separate strong and weak evidence on the page when mixed.
- For **safety, compliance, legal, or health** claims, require **explicit** sourcing or clear **deferral** to qualified professionals—do not present speculation as fact.

---

## Entity-first (named real-world subjects)

**Named** products, organizations, people, sites, or major systems that recur across pages should eventually earn an **`entities/`** page: one canonical title, short scope, links outward to concepts and source-notes. **Concepts** remain for ideas; **entities** are for specific things when the vault needs stable cross-links. Until an entity exists, link via topics and source-notes; add the entity when duplication becomes painful.

---

## Maintaining `wiki/index.md`

- `index.md` is the **catalog and navigation surface** agents should read first.
- Organize by **page category** (overview, entities, concepts, topics, source-notes, analyses, comparisons, timelines, glossary).
- Each entry: **relative link** + **one-line description**.
- After adding/removing/renaming pages, update `index.md`. Run `uv run python scripts/rebuild_index.py` to compare index links to files on disk.

---

## Maintaining `wiki/log.md`

- **Append-only**: never rewrite or delete historical entries.
- New entries go **below** prior content unless the user explicitly migrates format (then log the migration in a new `policy` entry).
- Heading format (required):

```markdown
## [YYYY-MM-DD] ingest | Short source or batch title
## [YYYY-MM-DD] query | Short question summary
## [YYYY-MM-DD] lint | What was checked
## [YYYY-MM-DD] refactor | Scope of reorganization
## [YYYY-MM-DD] policy | Convention or AGENTS change
```

- Body: bullet summary of actions, files touched, and pointers to durable pages.

---

## Page taxonomy

Standard directories under `wiki/`:

| `page_type` | Typical path | Role |
|-------------|--------------|------|
| `overview` | `overview.md` | North-star summary of the wiki’s domain |
| `source_note` | `source-notes/` | Grounding note for a raw source |
| `entity` | `entities/` | Named subject (person, org, product, paper) |
| `concept` | `concepts/` | Idea or term of art |
| `topic` | `topics/` | Thematic bucket spanning entities/concepts; often a **hub** for routing |
| `analysis` | `analyses/` | Argument, evaluation, synthesis; may include procedure-shaped pages in this repo |
| `comparison` | `comparisons/` | Structured A vs B |
| `timeline` | `timelines/` | Chronology |
| `glossary` | `glossary/` | Definition-first entries |
| `operating_doc` | (rare; or root) | How the repo itself is operated |

Forks may add optional YAML (e.g. `page_subtype`) for guide-like analyses; the template validator focuses on `title` and `page_type` where required.

---

## Naming conventions

- **Filenames**: `kebab-case.md` exclusively.
- **Titles**: Sentence case or title case — **one canonical title per page** in `title` frontmatter.
- **Stability**: Prefer renaming by adding `aliases` frontmatter and updating links; avoid churn.

---

## Linking conventions

- Use **relative Markdown links** only: `[text](../concepts/foo.md)` not absolute repo paths.
- **Obsidian**: `[[wiki links]]` optional; portable links must still exist as `.md` relatives for MkDocs-oriented tooling.
- **Wikilinks**: If you use `[[...]]`, ensure a parallel `.md` relative link exists for non-Obsidian consumers (CI may optionally enforce this later).

---

## Citation conventions

- When a claim depends on a raw source, cite **stable path + optional excerpt id**:

```markdown
See [raw/processed/2026/example.md](../../raw/processed/2026/example.md) — section “Key finding”.
```

- Prefer `source_ids` in frontmatter for machine-checkable linkage.

---

## Frontmatter schema

Optional YAML frontmatter is encouraged. Common fields:

| Field | Meaning |
|-------|---------|
| `title` | Display title (should match index) |
| `page_type` | One of the taxonomy types |
| `status` | `draft` \| `active` \| `deprecated` |
| `created` | ISO date |
| `updated` | ISO date |
| `source_count` | Integer (optional) |
| `source_ids` | List of stable ids or raw paths |
| `aliases` | Alternate titles |
| `tags` | List of short tokens |
| `supersedes` / `superseded_by` | For deprecation chains |
| `confidence` | `low` \| `medium` \| `high` (epistemic) |
| `review_status` | `unreviewed` \| `reviewed` \| `stale` |

**Rules**:

- `wiki/overview.md`, entity/concept/analysis/comparison/timeline pages: **must** include `title` and `page_type` for validation.
- `wiki/log.md` and `wiki/index.md`: **no** required frontmatter.

---

## Conflict and contradiction handling

- **Do not silently overwrite** competing claims. Prefer:
  - same page: add dated subsection with evidence and confidence; or
  - split: new analysis page with `supersedes` linkage.
- Call out unresolved tension explicitly; log significant merges in `log.md`.

---

## Stale-claim handling

- Mark uncertain or dated material with `review_status: stale` or a visible callout.
- Prefer incremental updates; if replacing, use `superseded_by` and keep a short redirect note in the old page body.

---

## Orphan page handling

- A page is **orphan** if no other wiki page links to it **and** it is not listed in `index.md`. Validation reports orphans; fix by adding inbound links or index entries.

---

## Proposing new pages

1. Pick `page_type` and path per taxonomy.
2. Copy from `templates/` using `uv run python scripts/scaffold_page.py`.
3. Fill frontmatter, write minimal viable content, cross-link, update `index.md`, append `log.md`.

---

## Filing answers back into the wiki

- Ephemeral chat answers → durable **`analyses/`** or **`concepts/`** page when reuse is likely.
- Include **question context**, **answer summary**, **links** to sources and related wiki pages.
- Log under `query` with pointer to the new page.

---

## Incremental maintenance

- **Prefer small, frequent edits** over full rewrites.
- When refactoring, batch by theme; log under `refactor`.
- Reserve large-scale reorg for explicit user approval.

---

## Raw sources are immutable

- **Never** edit files in `raw/processed/` except **append-only** logs if a dedicated log file exists and policy allows.
- Corrections belong in **wiki** or new raw notes with clear provenance, not silent fixes to archived sources.

---

## Log is append-only history

- Do not delete or rewrite past `## [...]` entries in `wiki/log.md`.
- Typo fixes: only if they do not change meaning; prefer a new correction entry.

---

## Preserving user intent and provenance

- Follow explicit user instructions for scope and tone.
- When summarizing sources, preserve distinctions the user cares about.
- Prefer quoting short phrases from raw over paraphrase when ambiguity is high.

---

## Relative links for Obsidian and MkDocs

- Wiki links must work when opened as a folder vault in Obsidian **and** when processed by static analyzers.
- Avoid spaces in filenames; use `kebab-case.md`.
- For assets, prefer `raw/assets/` or documented attachment paths in `docs/operations/obsidian.md`.

---

## Agent session checklist

1. Read `AGENTS.md` (this file) and `wiki/index.md`.
2. Identify layer: raw vs wiki vs docs change.
3. Run `uv run python scripts/validate_wiki.py` before and after substantive edits.
4. Update `wiki/index.md` when navigation should change; update **hubs** when adding siblings in the same cluster.
5. Append `wiki/log.md` for ingest/query/lint/refactor/policy work.
6. Keep commits scoped and messages descriptive.

---

## Definition of done

| Task | Done when |
|------|-----------|
| **Ingest** | Raw filed; source-notes grounded; **activation** decided and routing/hubs updated when material warrants it; log + index updated; validator passes |
| **Query** | Answer cites wiki/raw; durable page created/updated if needed; log appended |
| **Lint** | Validator clean (`--strict` in CI); orphans/titles addressed or explicitly deferred in log |

---

## Scripts reference

| Script | Role |
|--------|------|
| `scripts/bootstrap.py` | Create missing dirs/files; optional rename placeholders |
| `scripts/validate_wiki.py` | Repository integrity checks |
| `scripts/validate_docs_links.py` | Internal link checks for `docs/` (handbook) |
| `scripts/rebuild_index.py` | Audit or regenerate index sections |
| `scripts/append_log.py` | Append a correctly formatted log entry |
| `scripts/scaffold_page.py` | New page from `templates/` |
| `scripts/ingest_pdf.py` | PDF text → markdown under `raw/processed/` |
| `scripts/render_taxonomy_doc.py` | Regenerate `docs/reference/page-taxonomy.md` from `AGENTS.md` + `templates/` |
| `scripts/wiki_search.py` | Optional regex search across `wiki/` markdown |
| `scripts/wiki_wikilinks.py` | Report unresolved `[[wikilinks]]` (missing targets) |
| `scripts/intake_inbox.py` | Optional report on files in `raw/inbox/` |

---

## Non-goals

- Opaque databases, proprietary formats, or undocumented codegen as the source of truth.
- Turning `wiki/` into an unbounded dump without structure.

When uncertain, **add a note in the wiki**, **cite raw**, and **log the decision**.
