#!/usr/bin/env python3
"""
Initialize missing directories and optional MkDocs site title.

Safe to run multiple times. Does not overwrite wiki pages.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

DIRS = [
    "wiki/entities",
    "wiki/concepts",
    "wiki/topics",
    "wiki/analyses",
    "wiki/comparisons",
    "wiki/timelines",
    "wiki/glossary",
    "wiki/source-notes",
    "raw/inbox",
    "raw/processed",
    "raw/assets",
    "docs/workflows",
    "docs/conventions",
    "docs/operations",
    "examples/raw",
    "examples/wiki",
    "templates",
    "tests",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap LLM Wiki repo directories")
    parser.add_argument(
        "--site-name",
        default=None,
        help='If set, set mkdocs.yml "site_name:" to this value (string).',
    )
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="Repository root")
    args = parser.parse_args()
    root: Path = args.root.resolve()

    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    if args.site_name:
        mk = root / "mkdocs.yml"
        if mk.is_file():
            text = mk.read_text(encoding="utf-8")
            new = re.sub(r"^site_name:\s.*$", f"site_name: {args.site_name}", text, flags=re.MULTILINE)
            mk.write_text(new, encoding="utf-8")
            print(f"Updated site_name in {mk}")

    print(f"Bootstrap complete under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
