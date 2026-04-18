# LLM Wiki Template

A **GitHub template repository** for a structured, **LLM-maintained markdown wiki**: immutable `raw/` sources, a compounding `wiki/` synthesis layer, and an operator handbook in `docs/` published with **MkDocs (Material)**. It is designed for personal research, project intelligence, reading companions, due diligence, and small team knowledge bases—not a generic notes dump.

## What you get

- **Clear layers:** `raw/` (evidence) vs `wiki/` (maintained model) vs `docs/` (how to run the system).
- **Agent contract:** [`AGENTS.md`](AGENTS.md) is the highest-priority schema for humans and automation (ingest / query / lint, append-only log, no silent raw edits).
- **Navigation:** [`wiki/index.md`](wiki/index.md) is the catalog; [`wiki/log.md`](wiki/log.md) is the append-only chronology.
- **Integrity:** `scripts/validate_wiki.py` checks links, index coverage, log headings, frontmatter rules, orphans, and more (`--strict` in CI); `scripts/validate_docs_links.py` checks the MkDocs handbook under `docs/`.
- **Tooling:** Bootstrap, scaffold, append-log, index audit, PDF ingest, optional wiki search / wikilink reports. Dependencies live in **`pyproject.toml`** with **runtime** vs **docs** vs **dev** [groups](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-groups); use **`uv sync --all-groups`** for a full dev environment (`uv.lock` pins everything).
- **CI + Pages:** GitHub Actions runs tests, validation, and `mkdocs build --strict`; pushes to `main` deploy the handbook to GitHub Pages.

## Create a new repository from this template

On GitHub: **Use this template** → create your repository → clone locally. Then optionally:

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
python3 scripts/bootstrap.py --site-name "My Wiki"
uv sync --all-groups
make docs-serve
```

Open **`wiki/`** (or the repo root) in **Obsidian** as a vault. Read [`docs/quickstart.md`](docs/quickstart.md) for the full path: clone → Obsidian → local docs → Pages.

## Repository layout

| Path | Role |
|------|------|
| [`AGENTS.md`](AGENTS.md) | Operating contract for agents |
| [`wiki/`](wiki/) | Taxonomy pages, `index.md`, `log.md` |
| [`raw/`](raw/) | Inbox, processed sources, assets (immutable after filing) |
| [`docs/`](docs/) | MkDocs handbook (architecture, workflows, conventions) |
| [`scripts/`](scripts/) | Validation and helpers |
| [`templates/`](templates/) | Page and checklist templates |
| [`examples/`](examples/) | Isolated demos (not wired into the live wiki) |
| [`tests/`](tests/) | Pytest coverage for validators and conventions |
| [`pyproject.toml`](pyproject.toml), [`uv.lock`](uv.lock) | Pinned Python dependencies (uv) |

## Workflows (high level)

1. **Ingest** — add raw material, write `source-notes`, update synthesis pages, refresh `index.md`, append `log.md`, run the validator.
2. **Query** — answer from the wiki + citations; file durable pages under `analyses/` or `concepts/` when useful; log the query.
3. **Lint** — periodic passes for links, index alignment, stale claims, duplicates; log the lint.

Details: [`docs/workflows/`](docs/workflows/).

## Scripts

```bash
uv sync --all-groups                            # runtime + docs (MkDocs) + dev (pytest, ruff, …)
uv run python scripts/bootstrap.py              # create missing dirs; optional --site-name
make validate                                   # wiki strict + docs/ link check (see Makefile)
uv run python scripts/rebuild_index.py          # audit wiki/index.md vs files on disk
uv run python scripts/append_log.py --kind ingest --title "..."  # append wiki/log.md
uv run python scripts/scaffold_page.py --type concept --title "My concept"
uv run python scripts/ingest_pdf.py raw/inbox/your-file.pdf   # PDF → raw/processed/…/… .md
```

**Shortcuts:** **`Makefile`** — `make docs-serve`, `make docs-build`, `make test`, `make bootstrap`, `make validate`. **`just`** — same recipes in `justfile` (e.g. `just validate`, `just docs-serve`). Optional: `uv run pre-commit install` after sync (see `docs/quickstart.md`).

## Documentation site

- **Local preview:** `uv sync --all-groups && make docs-serve` (or `uv run mkdocs serve` after `scripts/render_taxonomy_doc.py`)
- **Publish:** enable **GitHub Pages** with the **GitHub Actions** source; the workflow in `.github/workflows/docs.yml` builds and deploys on `main`.

## Conventions

- **Filenames:** `kebab-case.md` in taxonomy folders; see validator for exceptions (`index`, `log`, `overview` at `wiki/` root).
- **Links:** relative `.md` links for wiki and raw (Obsidian / GitHub / tooling). The published handbook may link to GitHub blob URLs for files outside `docs/` so MkDocs strict builds stay clean.

## License

See [`LICENSE`](LICENSE).

## Upstream

Template source: [`sempervent/llm-wiki-template`](https://github.com/sempervent/llm-wiki-template). After forking, replace GitHub URLs in `docs/` that point at this template with your own repository if you publish the handbook.
