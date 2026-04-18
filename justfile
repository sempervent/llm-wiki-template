# Task runner (https://github.com/casey/just) — mirrors Makefile shortcuts.
# Install: https://github.com/casey/just#installation
# Usage: `just` or `just --list`

uv := "uv"

# Default: list recipes
default:
    @just --list

sync:
    {{uv}} sync --all-groups

bootstrap: sync
    {{uv}} run python scripts/bootstrap.py

validate-docs:
    {{uv}} run python scripts/validate_docs_links.py

taxonomy-render:
    {{uv}} run python scripts/render_taxonomy_doc.py

taxonomy-check:
    {{uv}} run python scripts/render_taxonomy_doc.py --check

validate: sync
    {{uv}} run python scripts/validate_wiki.py --strict
    {{uv}} run python scripts/validate_docs_links.py

test: sync
    {{uv}} run pytest

docs-build: sync taxonomy-render
    {{uv}} run mkdocs build --strict

docs-serve: sync taxonomy-render
    {{uv}} run mkdocs serve

check: sync
    {{uv}} run python scripts/validate_wiki.py --strict
    {{uv}} run python scripts/validate_docs_links.py
    {{uv}} run pytest
    {{uv}} run python scripts/render_taxonomy_doc.py --check
    {{uv}} run mkdocs build --strict
