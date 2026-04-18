"""Shared helpers for wiki paths, frontmatter, and link parsing."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
LOG_HEADING_PATTERN = re.compile(
    r"^## \[(?P<date>\d{4}-\d{2}-\d{2})\] (?P<kind>ingest|query|lint|refactor|policy) \| (?P<title>.+)$"
)
KEBAB_MD_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")


def repo_root_from_scripts() -> Path:
    """Fallback when the current directory is not the repository root."""
    return Path(__file__).resolve().parent.parent


def infer_repo_root(explicit: Path | None) -> Path:
    """
    Resolve repository root: explicit --root, else cwd if it looks like this repo
    (contains AGENTS.md), else the package checkout next to scripts/.
    """
    if explicit is not None:
        return explicit.resolve()
    cwd = Path.cwd().resolve()
    if (cwd / "AGENTS.md").is_file():
        return cwd
    return repo_root_from_scripts()


FM_HEADER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def load_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter dict, body). Empty dict if no frontmatter."""
    m = FM_HEADER.match(text)
    if not m:
        return {}, text
    fm_raw = m.group(1)
    body = text[m.end() :]
    try:
        data = yaml.safe_load(fm_raw) or {}
        if not isinstance(data, dict):
            return {}, text
        return data, body
    except yaml.YAMLError:
        return {}, text


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Return list of (label, target) for markdown links."""
    return [(m.group(1), m.group(2).strip()) for m in LINK_PATTERN.finditer(text)]


def normalize_link_target(target: str) -> str | None:
    if not target:
        return None
    if target.startswith(("http://", "https://", "mailto:")):
        return None
    if target.startswith("#"):
        return None
    # Strip anchor and query
    t = target.split("#", 1)[0].split("?", 1)[0].strip()
    return t if t else None


def resolve_markdown_path(base_file: Path, target: str, root: Path) -> Path | None:
    """Resolve a relative markdown link to an absolute path under root, or None if external."""
    norm = normalize_link_target(target)
    if norm is None:
        return None
    resolved = (base_file.parent / norm).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def is_kebab_md(name: str) -> bool:
    return bool(KEBAB_MD_PATTERN.match(name))


def requires_frontmatter_schema(rel_wiki_path: Path) -> bool:
    """Paths that must include title + page_type in frontmatter."""
    parts = rel_wiki_path.parts
    if len(parts) < 2 or parts[0] != "wiki":
        return False
    if len(parts) == 2 and parts[1] == "overview.md":
        return True
    if len(parts) < 3:
        return False
    top = parts[1]
    return top in {
        "entities",
        "concepts",
        "topics",
        "analyses",
        "comparisons",
        "timelines",
        "glossary",
        "source-notes",
    }
