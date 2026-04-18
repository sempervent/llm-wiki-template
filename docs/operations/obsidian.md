# Obsidian settings

## Opening the vault

- **Whole repo:** open the repository root to access `wiki/`, `raw/`, and `docs/` in one tree.
- **Wiki only:** open `wiki/` as the vault if you want a minimal graph.

## Recommended settings

- **Files & links → Automatically update internal links:** useful when renaming with Obsidian; still run `scripts/validate_wiki.py` after bulk renames.
- **New link format:** Relative path to file (aligns with MkDocs and GitHub).

## Attachments

- Store binaries under `raw/assets/` (or a dedicated `attachments/` path you document once).
- Reference from markdown with relative links: `../../raw/assets/diagram.png`.
- Avoid committing huge binaries without Git LFS; keep the template lean.

## Graph view

Cross-link entities, concepts, and analyses liberally. Prefer stable titles in frontmatter so the graph stays readable after refactors.
