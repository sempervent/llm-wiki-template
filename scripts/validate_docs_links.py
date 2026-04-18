#!/usr/bin/env python3
"""
Validate relative markdown links inside docs/ (handbook) resolve to existing files.

Complements scripts/validate_wiki.py, which focuses on wiki/ and repository structure.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from wiki_common import extract_markdown_links, infer_repo_root, normalize_link_target, resolve_markdown_path


def collect_docs_md(root: Path) -> list[Path]:
    docs = root / "docs"
    if not docs.is_dir():
        return []
    return sorted(docs.rglob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check internal links in docs/*.md")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    args = parser.parse_args()
    root = infer_repo_root(args.root)
    errors: list[str] = []

    for path in collect_docs_md(root):
        rel = path.resolve().relative_to(root)
        text = path.read_text(encoding="utf-8")
        for _label, target in extract_markdown_links(text):
            norm = normalize_link_target(target)
            if norm is None:
                continue
            # Handbook links should stay inside docs/ for portability
            resolved = resolve_markdown_path(path, norm, root)
            if resolved is None:
                continue
            if not resolved.is_file():
                errors.append(f"Broken link in {rel}: {norm!r} -> {resolved}")

    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
