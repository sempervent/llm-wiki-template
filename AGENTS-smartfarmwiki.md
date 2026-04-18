# AGENTS.md — Operating contract

This file is the **highest-priority behavioral contract** for any automated or human agent working in this repository. When instructions conflict, **follow this document first**, then `README.md`, then task-specific prompts.

---

## Mission

This repository implements an **LLM-maintained markdown wiki**: a persistent, compounding knowledge base where:

- **`raw/`** holds **immutable** source material (notes, imports, excerpts, files).
- **`wiki/`** holds the **agent-authored synthesis** (business plan packages, entities, concepts, timelines, glossary, analyses, **procedural guides** in `analyses/` via `page_subtype`, cross-links).
- **`docs/`** holds the **operator handbook** for humans and agents (read in-repo); it explains *how* the system works, not the domain knowledge itself. (In this fork, the **MkDocs site** is built from **`wiki/`** only; see `mkdocs.yml` and `docs/operations/publishing.md`.)

The **mechanical goal** is **deterministic, inspectable, markdown-first** workflows: plain files, clear paths, validation scripts, and reproducible doc builds.

### Domain mission and prose (Smart Farm Wiki)

**Why not duplicate long mission prose here:** `AGENTS.md` must stay a **short, stable contract**—rules agents load every session. **Mission statements, audience, values, and voice** belong in the wiki so they **version with synthesis**, appear on the **published site**, and can evolve without bloating the contract file.

**Canonical page:** [`wiki/concepts/smart-farm-wiki-mission-and-values.md`](wiki/concepts/smart-farm-wiki-mission-and-values.md) — mission, vision, audience, authoring values, and voice. Agents shaping **tone** or **scope** for new pages should read it alongside [`wiki/overview.md`](wiki/overview.md).

**Reasoning summary:** Separation keeps **behavioral law** (this file) distinct from **intellectual purpose** (wiki)—reducing merge conflict on policy vs prose, and keeping “what we believe about small-scale ag and appropriate technology” **editable by the same ingest/query workflow** as other concepts.

---

## Layer definitions

| Layer | Purpose | Mutable by agent? |
|-------|---------|-------------------|
| `raw/` | Provenance-grounded sources (markdown imports, **PDFs**, and other files); inbox → processed pipeline | **Append / file new sources only. Never edit processed or alter meaning of stored sources.** |
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

---

## Mandatory workflows

### Ingest

1. Add or confirm raw material under `raw/inbox/` (or processed pipeline per `docs/workflows/ingest.md`).
   - **PDFs** are first-class sources: move each to `raw/processed/...` under a stable **kebab-case** basename, run `uv run python scripts/pdf_to_markdown.py <path-to.pdf>` (or `--all-raw`) so a sibling **`*-extracted.md`** machine extract exists; the **PDF remains canonical** for figures and layout. Source-notes for PDFs must cite **both** the `.pdf` and the `*-extracted.md` in the body (and `source_ids` includes the `.pdf` path). See `docs/workflows/ingest.md` and `scripts/validate_raw_pdf_links.py` / `validate_wiki.py --raw-pdf-links` when the full corpus is local.
2. Create or update **`source-notes`** in `wiki/source-notes/` pointing to stable `raw/` paths.
3. Update relevant entity/concept/topic pages; add cross-links.

### Ingest activation rule

Ingestion is not complete when a source-note exists. Ingestion is complete only when the agent has evaluated whether the new source should also:

- update a canonical page
- update a comparison or matrix
- update a guide, runbook, or standard
- update a site-intelligence or entity page
- update a hub or routing surface
- add a new durable synthesis page when no canonical destination yet exists

For every meaningful ingest batch, the agent should decide explicitly:

1. **Source-note only**
2. **Source-note + canonical page update**
3. **Source-note + matrix/comparison/checklist update**
4. **Source-note + new synthesis artifact**
5. **Source-note + deferred follow-up note in `wiki/log.md`**

If the source affects execution, architecture, business logic, risk, safety, infrastructure, or site intelligence, prefer updating canonical pages or operational artifacts rather than leaving the knowledge trapped in source-notes.

### Source-note Evidence summary (integration, not CI)

For **hub**, **batch**, and **official cluster** source-notes that back **execution** (business plan, parcels, off-grid, sensors, platform, backup/DR, observability), add an **Evidence summary** block per [`wiki/concepts/source-note-abstract-and-evidence-pattern.md`](wiki/concepts/source-note-abstract-and-evidence-pattern.md): **abstract**, **authority mix**, **decision relevance**, **canonical wiki links**, **public-safe key claims**, **open questions**. **Not** required for every minimal single-file note. A note may remain **capture-only** until activation—log deferrals when material.

### When to add matrices, guides, standards, or checklists

| Artifact | Prefer when |
|----------|-------------|
| **Matrix / comparison** | Readers repeatedly need **A vs B** or **many SKUs/classes** in one view; **extend** an existing comparison before creating a sibling. |
| **Standard** (`page_subtype: standard`) | A **short norm** (“must be true”) with stable **gates**—link to **guides** for long sequences. |
| **Guide** (`operational_guide`) | Ordered **steps** or **doctrine spine** with routing. |
| **Checklist** | **Repeatable** field or ops verification—often a **section** inside a standard, guide, or **local evidence** template before a new page. |

Package strategy for procedures: [`wiki/topics/procedural-guides-package-strategy-smart-farm-wiki.md`](wiki/topics/procedural-guides-package-strategy-smart-farm-wiki.md).

### Structural validation vs integration quality

- **Structural** (CI): `scripts/validate_wiki.py --strict`—required files, index coverage, resolvable wiki links, log headings, frontmatter on schema pages, kebab-case, duplicate titles / orphans (heuristic). Optional `validate_raw_pdf_links.py` / `--raw-pdf-links` when the full `raw/` tree is present.
- **Integration** (policy, not automatically fail-able): ingest **activation** completed, Evidence summaries on **high-value** source-notes, **canonical** pages and **hubs** updated so evidence is not **trapped** in `source-notes/`. Treat **structural pass + missing activation** as **technical debt**—record in `wiki/log.md` when significant.

4. **Append** `wiki/log.md` with `ingest` entry (see Log format).
5. **Update** `wiki/index.md` if new pages were added or titles changed.
6. Run `uv run python scripts/validate_wiki.py` before commit.

### Query

1. Answer from `wiki/` + cited `raw/` paths; do not invent provenance.
2. If the answer should persist, **create or update** a durable wiki page (often `analyses/` or `concepts/`) and link it from `index.md` when appropriate.
3. **Append** `wiki/log.md` with `query` entry summarizing the question and where the answer lives.

### Lint

Periodic hygiene: link integrity, orphan reduction, stale-claim review, duplicate title checks, index alignment.

1. Run `uv run python scripts/validate_wiki.py` (use `--strict` in CI).
2. Fix or ticket broken links; add missing index entries for intentional pages.
3. **Append** `wiki/log.md` with `lint` entry.

---

## Maintaining `wiki/index.md`

- `index.md` is the **catalog and navigation surface** agents should read first.
- Organize by **page category** (overview, **business plan packages**, entities, concepts, topics, source-notes, analyses, comparisons, timelines, glossary). For **themed** entry points without splitting the full analyses list, link **[`wiki/topics/wiki-navigation-and-structural-hubs.md`](wiki/topics/wiki-navigation-and-structural-hubs.md)** from the overview or analyses intro.
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
| `topic` | `topics/` | Thematic bucket spanning entities/concepts |
| `analysis` | `analyses/` | Argument, evaluation, synthesis, **or** procedure-shaped pages (runbooks, how-tos) that remain here for validation/tooling consistency |
| `comparison` | `comparisons/` | Structured A vs B |
| `timeline` | `timelines/` | Chronology |
| `glossary` | `glossary/` | Definition-first entries |
| `operating_doc` | (rare; or root) | How the repo itself is operated |

**Business plan packages** (`wiki/business-plan/`): **first-class** navigation pages for a **named** business plan (e.g. East Tennessee two-site). They **do not replace** analysis chapters in `analyses/`—they provide a **stable spine** (reading order, artifact tables, links to critique and repo wiring). Use `page_type: topic` unless a dedicated type is introduced later.

### Analysis subtypes and guide-shaped pages (`page_subtype`)

Procedure runbooks, stepwise operator guides, and **standards** often live under `analyses/` because they share the same validation rules as other syntheses. To make them **first-class in metadata** without splitting directories, use optional YAML:

| `page_subtype` | Typical content | Notes |
|----------------|-----------------|--------|
| *(omitted)* | Default analysis | Essay, audit, synthesis, matrix—no implied procedure. |
| `operational_guide` | Checklist / sequence runbooks (e.g. Pi k3s provisioning **hub** + child sequence pages) | Opening section should state **mandatory** vs **optional HA** steps when applicable. |
| `standard` | Operator **norms** (hostnames, iSCSI, roles)—short durable bar | Pair with **`operational_maturity`** when the standard has been exercised on real infra. |
| `meta_audit` | IA / repository / ownership audits | Distinct from domain “essay” analyses; links **hubs**, does not replace them. |
| `query_synthesis` | Time-stamped answers to ad-hoc questions | If doctrine becomes permanent, **fold** into a canonical page and add routing. |

**Standards** may also be `topic` pages when they are purely narrative; use `page_type: analysis` + `page_subtype: standard` when the page is checklist-heavy and validated like other analyses.

### Guides vs runbooks vs standards (within `analyses/`)

Procedural content stays under **`wiki/analyses/`** for validation and MkDocs consistency. Distinctions are **semantic** (reader intent), not separate directories:

| Reader intent | Metadata / convention |
|---------------|------------------------|
| **Standard** (norms) | `page_subtype: standard` — short **bars**; link out to guides for full sequences |
| **Guide** (how-to, drill, doctrine spine with operator routing) | `page_subtype: operational_guide` |
| **Runbook** (incident / degraded mode) | `operational_guide` + prefer **`runbook-*.md`** filename (or **Runbook —** title) |
| **Essay / audit** | Default analysis (`page_subtype` omitted or `meta_audit` / `query_synthesis`) |

**Package strategy** (where they live, maturity labels, linking to architecture and entities): [`wiki/topics/procedural-guides-package-strategy-smart-farm-wiki.md`](wiki/topics/procedural-guides-package-strategy-smart-farm-wiki.md).

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

## Public corpus vs private or sensitive material

- **`raw/`** may be **large, local-only, or gitignored**; CI and clones may not have every file. **Do not** treat missing `raw/` targets in validation as permission to weaken provenance in the wiki—keep stable paths, and run `validate_wiki.py --raw-pdf-links` when the full corpus is present.
- **MkDocs** publishes **`wiki/`** as the public-facing site; **`docs/`** is the operator handbook. Paths under `raw/` in wiki markdown are **neutralized** in HTML builds so public readers do not get **broken navigable links** to files that are not shipped—see `docs/operations/raw-corpus-and-publishing.md`. **Obsidian** authors may still open `raw/` locally.
- **Secrets and operational security**: Do not commit **passwords, keys, hostnames, or internal IPs** into `wiki/` or `raw/` unless policy explicitly allows and rotation is understood. Prefer **placeholders** (`BROKER_LABEL`, `SITE_FARM`) in published pages and keep **site-specific truth** in **private** runbooks or encrypted stores outside the repo.

---

## Canonicalization before proliferation

- Before adding a **new** analysis or topic page, search **`wiki/index.md`**, **`wiki/analyses/domain-content-overview.md`**, and the relevant **topic hub** (e.g. [`wiki/topics/two-site-smart-farm-operations.md`](wiki/topics/two-site-smart-farm-operations.md)) for an existing **canonical** page (business-plan core, reference architecture, runbook parent).
- **Extend** the canonical page with a dated subsection, a table row, or a “See also” block rather than spawning a **parallel essay** that overlaps scope. If overlap is unavoidable, add **`supersedes` / `superseded_by`** (or explicit “routing” sections pointing to the canonical home) and log the decision in `wiki/log.md`.
- Meta and repository-structure audits belong in **`analyses/`** with clear titles; they should **link** to domain hubs rather than replacing them.

### Operational and guide-shaped content

- **One procedure owner per subject cluster** (e.g. Pi k3s: strategy page + one guide hub linking sequence pages). New checklists should attach to that hub or justify a new `page_subtype: operational_guide` scope in `wiki/log.md`.
- **Standards** (short norms) **vs** **guides** (long sequences): prefer a standard page + guide hub pair over two guides with duplicated outlines.
- **First-class guides**: treat procedural pages as durable products—tag **`operational_maturity`**, link **standards** + **entities** + **architecture**, and follow the **package strategy** page above.
- Use [`wiki/topics/wiki-navigation-and-structural-hubs.md`](wiki/topics/wiki-navigation-and-structural-hubs.md) when `index.md` feels too flat—do **not** duplicate the full analysis list there.

---

## Entity-first rule (persistent real-world subjects)

- **Named products**, **organizations**, **operating sites** (homestead vs production parcel **roles**), **infrastructure systems** (water, power, field telemetry as a stack), **breeds**, **regulated agencies**, and **major software projects** that appear in multiple pages should eventually have an **`entities/`** page: one **canonical title**, `page_type: entity`, short **scope** (what the page is for), and links **out** to concepts, comparisons, and source-notes. Site entities use **planning labels** (`SITE_HOME`, `SITE_FARM`) and **do not** assert uncommitted parcel facts.
- **Concepts** remain for **ideas** (e.g. “LoRaWAN” as technology); **entities** are for **specific** things (e.g. a particular **open-source project** or **company**) when the vault needs stable cross-links and index entries.
- Until an entity exists, link to **source-notes** and **topics**; add the entity when the third or fourth page would duplicate the same introduction text.

---

## Hub maintenance

- **Topic hubs** and **`wiki/index.md`** are **routing contracts**: when you add a sibling page (new runbook, comparison, or business-plan chapter), update the **hub table** or index section so the new page is **discoverable** without relying on search alone.
- **Strategic-audit** and **implementation-backlog** pages are **maps**, not substitutes for hubs—keep **`domain-content-overview`** and topic hubs aligned when navigation changes.

---

## Page ownership (canonical subjects)

- A **canonical page** **owns** durable scope for a **cluster** (business plan package + framework, reference architecture + SoR + field telemetry, validation stack, two-site operating model). **Major** additions to the subject should land **there** first, or in a clearly scoped **child** analysis that **links upward** in the opening section.
- **Analyses** that only **support** a canonical page (runbooks, pilots, query syntheses) should **not** copy the canonical page’s **outline**; add a **Routing** paragraph if overlap could confuse readers.
- **Ownership map** (clusters, risks, entity backlog): [`wiki/analyses/structural-audit-page-ownership-entity-gaps-and-hub-routing.md`](wiki/analyses/structural-audit-page-ownership-entity-gaps-and-hub-routing.md). Update that audit when **ownership** or **merge** decisions change materially—log significant changes in `wiki/log.md`.
- **Agritourism vs production-led** scenarios are **different** products; cross-link as **alternates**, do not merge without explicit `supersedes` and human intent.

---

## Claim strength and source authority

- Prefer **authoritative** sources for upgradable claims: **Extension**, **USDA / NRCS**, **land-grant** publications, **peer-reviewed** work, vendor **primary documentation**, and **standards** (ITU, IEEE, RFC). Label **forums, blogs, and chat exports** as **anecdotal** unless corroborated.
- Use frontmatter **`confidence`** and **`review_status`** honestly. When mixing strong and weak sources on one page, **separate** them visually (subsections or tables). **Do not** upgrade **“might”** to **“does”** without a cited source or a labeled assumption.
- **Regulatory and safety** claims (food safety, animal health, electrical work) require **explicit** sourcing or **deferral** to professionals—see [`wiki/concepts/smart-farm-wiki-mission-and-values.md`](wiki/concepts/smart-farm-wiki-mission-and-values.md).

---

## Frontmatter schema

Optional YAML frontmatter is encouraged. Common fields:

| Field | Meaning |
|-------|---------|
| `title` | Display title (should match index) |
| `page_type` | One of the taxonomy types |
| `page_subtype` | Optional; see **Analysis subtypes** (e.g. `operational_guide`, `standard`, `meta_audit`, `query_synthesis`) |
| `status` | `draft` \| `active` \| `deprecated` — **repository / editorial lifecycle** for the page |
| `operational_maturity` | Optional; **`draft`** \| **`pilot_ready`** \| **`field_tested`** \| **`superseded`** — **how** **much** **real-world** **exercise** **the** **procedure** **has** **had** (orthogonal to `status`) |
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

**Operational maturity (optional)**:

- Use **`operational_maturity`** on **runbooks**, **standards**, and **guide hubs** where **deployment history** matters to readers.
- **`draft`**: structure present; not yet validated against live systems.
- **`pilot_ready`**: exercised in lab or constrained pilot; limitations documented.
- **`field_tested`**: used on real farm/homelab edge under stated constraints; drills or incidents inform updates.
- **`superseded`**: routing preserved for links; must pair with **`superseded_by`** (or explicit successor section) when replacing procedure content.
- Do **not** conflate with **`review_status`** (editorial review) or **`confidence`** (source epistemics).

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

1. Read `AGENTS.md` (this file) and `wiki/index.md`. For **navigation / IA** context, see [`wiki/topics/wiki-navigation-and-structural-hubs.md`](wiki/topics/wiki-navigation-and-structural-hubs.md) and [`wiki/analyses/structural-debt-audit-wiki-ia-and-operational-maturity.md`](wiki/analyses/structural-debt-audit-wiki-ia-and-operational-maturity.md). For **procedural how-tos and runbooks**, see [`wiki/topics/procedural-guides-package-strategy-smart-farm-wiki.md`](wiki/topics/procedural-guides-package-strategy-smart-farm-wiki.md). When authoring substantive **domain** synthesis, also read [`wiki/concepts/smart-farm-wiki-mission-and-values.md`](wiki/concepts/smart-farm-wiki-mission-and-values.md) for mission, audience, and voice alignment. Before creating **new** parallel analyses, apply **Canonicalization before proliferation**, check topic hubs, and consult [`wiki/analyses/structural-audit-page-ownership-entity-gaps-and-hub-routing.md`](wiki/analyses/structural-audit-page-ownership-entity-gaps-and-hub-routing.md) for **cluster ownership**.
2. Identify layer: raw vs wiki vs docs change.
3. Run `uv run python scripts/validate_wiki.py` before and after substantive edits.
4. Update `wiki/index.md` when navigation should change.
5. Append `wiki/log.md` for ingest/query/lint/refactor/policy work.
6. Keep commits scoped and messages descriptive.

---

## Definition of done

| Task | Done when |
|------|-----------|
| **Ingest** | Raw filed (for **PDFs**: sibling `*-extracted.md` + source-note cites both); source-notes + synthesis updated; log + index updated; validator passes; run `--raw-pdf-links` when the full `raw/` corpus is present locally |
| **Query** | Answer cites wiki/raw; durable page created/updated if needed; log appended |
| **Lint** | Validator clean (`--strict` in CI); orphans/titles addressed or explicitly deferred in log; hubs/index aligned after navigation changes (see **Hub maintenance**) |

---

## Scripts reference

| Script | Role |
|--------|------|
| `scripts/bootstrap.py` | Create missing dirs/files; optional rename placeholders |
| `scripts/validate_wiki.py` | Repository integrity checks; links under `raw/` need not resolve by default (corpus may be uncommitted); optional `--raw-pdf-links` with `--strict` when validating a full local corpus |
| `scripts/validate_raw_pdf_links.py` | PDF ↔ `*-extracted.md` pairing, wiki links into `raw/`, PDF source-note extract links; **default** warns on missing local files; **`--strict`** fails (public CI uses non-strict via pytest). Public MkDocs build neutralizes `raw/` links in HTML — see `docs/operations/raw-corpus-and-publishing.md` |
| `scripts/rebuild_index.py` | Audit or regenerate index sections |
| `scripts/append_log.py` | Append a correctly formatted log entry |
| `scripts/scaffold_page.py` | New page from `templates/` |
| `scripts/pdf_to_markdown.py` | PDF text → `*-extracted.md` beside the file (PyMuPDF; not OCR) |

---

## Structured derivative artifacts

When new sources materially improve a repeatable decision surface, the agent should prefer creating or updating structured derivative artifacts such as:

- comparison tables
- checklist matrices
- topology diagrams
- standards
- runbooks
- procedural guides
- decision-gate pages
- site-intelligence pages

Do not leave high-value operational knowledge only in narrative source-notes when it can be expressed more usefully as a structured artifact.

Examples:
- protocol sources → comparison page or sensor matrix
- backup/restore docs → DR comparison and runbook
- county/site evidence → site-intelligence page and missing-data register
- platform docs → standards, provisioning guides, and topology pages

--

## Evidence routing after ingestion

After ingesting important sources, the agent must check whether readers can actually find and use the resulting knowledge.

At least one of the following should usually be updated for high-value ingest work:
- a canonical page
- a topic hub
- `wiki/overview.md`
- `wiki/index.md`
- a business-plan package page
- a local site/county intelligence page
- a platform/off-grid/sensor hub

If the source-note is valuable but not yet routed from a relevant hub or canonical page, ingestion is incomplete.

--

## Non-goals

- Opaque databases, proprietary formats, or undocumented codegen as the source of truth.
- Turning `wiki/` into an unbounded dump without structure.

When uncertain, **add a note in the wiki**, **cite raw**, and **log the decision**.
