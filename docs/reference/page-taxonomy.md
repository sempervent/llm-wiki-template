# Page taxonomy (generated)

This page is produced by `scripts/render_taxonomy_doc.py` from the **Page taxonomy** section in `AGENTS.md` (repository root) and the `templates/` directory. **Do not edit by hand**—run:

```bash
uv sync --all-groups
uv run python scripts/render_taxonomy_doc.py
```

## Taxonomy (from AGENTS.md)

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

## Scaffold templates

Files in `templates/` used by `scripts/scaffold_page.py`:

- `analysis-page.md` — in repo root under `templates/analysis-page.md` (not part of the MkDocs site).
- `comparison-page.md` — in repo root under `templates/comparison-page.md` (not part of the MkDocs site).
- `concept-page.md` — in repo root under `templates/concept-page.md` (not part of the MkDocs site).
- `entity-page.md` — in repo root under `templates/entity-page.md` (not part of the MkDocs site).
- `glossary-page.md` — in repo root under `templates/glossary-page.md` (not part of the MkDocs site).
- `ingest-checklist.md` — in repo root under `templates/ingest-checklist.md` (not part of the MkDocs site).
- `lint-checklist.md` — in repo root under `templates/lint-checklist.md` (not part of the MkDocs site).
- `overview-page.md` — in repo root under `templates/overview-page.md` (not part of the MkDocs site).
- `source-note.md` — in repo root under `templates/source-note.md` (not part of the MkDocs site).
- `timeline-page.md` — in repo root under `templates/timeline-page.md` (not part of the MkDocs site).
