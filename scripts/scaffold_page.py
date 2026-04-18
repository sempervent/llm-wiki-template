#!/usr/bin/env python3
"""Create a new wiki page from a template."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from wiki_common import infer_repo_root

TEMPLATES = {
    "source_note": "source-note.md",
    "entity": "entity-page.md",
    "concept": "concept-page.md",
    "analysis": "analysis-page.md",
    "comparison": "comparison-page.md",
    "timeline": "timeline-page.md",
    "overview": "overview-page.md",
    "topic": "concept-page.md",
    "glossary": "glossary-page.md",
}

DIR_FOR_TYPE = {
    "source_note": "source-notes",
    "entity": "entities",
    "concept": "concepts",
    "topic": "topics",
    "analysis": "analyses",
    "comparison": "comparisons",
    "timeline": "timelines",
    "glossary": "glossary",
    "overview": "",
}


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "untitled"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a wiki page from templates/")
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(set(TEMPLATES.keys())),
        help="page_type / template selector",
    )
    parser.add_argument("--title", required=True, help="Page title")
    parser.add_argument("--slug", default=None, help="Filename stem (default: slugified title)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print target path and exit without writing",
    )
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    args = parser.parse_args()

    root = infer_repo_root(args.root)
    slug = args.slug or slugify(args.title)
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", slug):
        print("ERROR: slug must be kebab-case", file=sys.stderr)
        return 1

    sub = DIR_FOR_TYPE[args.type]
    wiki = root / "wiki"
    target_dir = wiki / sub if sub else wiki
    target_dir.mkdir(parents=True, exist_ok=True)
    out = target_dir / f"{slug}.md"

    tmpl_name = TEMPLATES[args.type]
    tmpl_path = root / "templates" / tmpl_name
    if not tmpl_path.is_file():
        print(f"ERROR: missing template {tmpl_path}", file=sys.stderr)
        return 1

    text = tmpl_path.read_text(encoding="utf-8")
    today = date.today().isoformat()
    text = text.replace("{{TITLE}}", args.title)
    text = text.replace("{{SLUG}}", slug)
    text = text.replace("{{DATE}}", today)
    text = text.replace("{{PAGE_TYPE}}", args.type if args.type != "topic" else "topic")

    if args.dry_run:
        print(out)
        return 0

    if out.exists():
        print(f"ERROR: {out} already exists", file=sys.stderr)
        return 1

    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")
    print("Next: add to wiki/index.md and run scripts/validate_wiki.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
