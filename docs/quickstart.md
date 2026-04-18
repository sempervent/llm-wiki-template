# Quickstart

## Create a repository from the template

1. Open the template on GitHub and choose **Use this template** → **Create a new repository**.
2. Name the repository (for example `my-research-wiki`) and clone it locally:

```bash
git clone https://github.com/YOUR_USER/my-research-wiki.git
cd my-research-wiki
```

3. Install **[uv](https://docs.astral.sh/uv/getting-started/installation/)** (one-time on your machine).

4. Create the virtual environment and install locked dependencies:

```bash
uv sync
```

5. Optional: set the MkDocs site title and ensure directories exist:

```bash
uv run python scripts/bootstrap.py --site-name "My Research Wiki"
```

## Open the wiki in Obsidian

1. In Obsidian: **Open folder as vault** → select the repository root (or only the `wiki/` folder if you prefer a smaller vault).
2. Use **Files** navigation; the catalog is `wiki/index.md` in your clone ([view on GitHub](https://github.com/sempervent/llm-wiki-template/blob/main/wiki/index.md)).

Recommended settings are described in [Obsidian notes](operations/obsidian.md).

## Run a local documentation preview

The published handbook lives in `docs/` and builds with MkDocs (Material theme).

```bash
uv sync   # if you have not synced yet
uv run mkdocs serve
```

Open the URL shown (typically `http://127.0.0.1:8000`).

## Publish to GitHub Pages

1. In the GitHub repository: **Settings → Pages → Build and deployment**.
2. Set **Source** to **GitHub Actions** (recommended with the included workflow).
3. Push to `main`; the workflow in `.github/workflows/docs.yml` builds MkDocs and deploys to Pages.

See [Publishing](operations/publishing.md) for permissions, concurrency, and branch rules.

## Validate the wiki locally

```bash
uv sync
uv run python scripts/validate_wiki.py --strict
uv run pytest
```

CI runs the same checks on pull requests and `main` (see `.github/workflows/ci.yml`).

## Updating dependencies

Edit version pins in `pyproject.toml`, then run `uv lock` and commit the updated `uv.lock`.
