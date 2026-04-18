# Publishing (MkDocs + GitHub Pages)

## What gets published

- The **handbook** in `docs/` is the MkDocs site (`mkdocs.yml`).
- The **wiki** in `wiki/` is optimized for Obsidian and Git; it is not automatically dumped into the MkDocs nav (keeps the handbook focused). You can add selected wiki pages to `mkdocs.yml` if you want them on the site.

## GitHub Actions

- **`.github/workflows/ci.yml`** — pull requests and pushes: `uv sync --frozen --all-groups`, wiki + docs validation, taxonomy check, pytest, MkDocs strict build.
- **`.github/workflows/docs.yml`** — pushes to `main` and manual dispatch: same steps plus upload to GitHub Pages (`actions/deploy-pages`).
- Uses concurrency to cancel superseded runs.

## Repository settings

Enable **GitHub Pages** with the **GitHub Actions** source. The first successful deploy creates the environment; no legacy `gh-pages` branch is required.

## Local build

```bash
uv sync
uv run mkdocs build --strict
```

Artifacts land in `site/` (gitignored).
