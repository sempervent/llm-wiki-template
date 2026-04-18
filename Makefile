# Convenience targets (requires GNU Make). Same recipes exist in ./justfile for `just`.
# Install everything with: make sync

UV ?= uv
PY := $(UV) run python

.PHONY: sync bootstrap validate validate-docs taxonomy-render taxonomy-check test docs-build docs-serve

sync:
	$(UV) sync --all-groups

bootstrap: sync
	$(PY) scripts/bootstrap.py

validate-docs:
	$(PY) scripts/validate_docs_links.py

taxonomy-render:
	$(PY) scripts/render_taxonomy_doc.py

taxonomy-check:
	$(PY) scripts/render_taxonomy_doc.py --check

validate: sync
	$(PY) scripts/validate_wiki.py --strict
	$(MAKE) validate-docs

test: sync
	$(UV) run pytest

docs-build: sync taxonomy-render
	$(UV) run mkdocs build --strict

docs-serve: sync taxonomy-render
	$(UV) run mkdocs serve
