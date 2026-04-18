#!/usr/bin/env python3
"""
Optional local full-text search over wiki markdown (stdlib regex; no index).

Example: uv run python scripts/wiki_search.py "synthesis layer" wiki
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from wiki_common import infer_repo_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Search wiki/*.md for a regex pattern")
    parser.add_argument("pattern", help="Python regex (case-insensitive)")
    parser.add_argument(
        "path",
        nargs="?",
        default="wiki",
        help="Directory under repo root to search (default: wiki)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root",
    )
    parser.add_argument(
        "-n",
        "--line-number",
        action="store_true",
        help="Prefix matches with file:line:",
    )
    args = parser.parse_args()
    root = infer_repo_root(args.root)
    search_root = (root / args.path).resolve()
    if not search_root.is_dir():
        print(f"ERROR: not a directory: {search_root}", file=sys.stderr)
        return 1
    try:
        cre = re.compile(args.pattern, re.IGNORECASE | re.MULTILINE)
    except re.error as e:
        print(f"ERROR: bad regex: {e}", file=sys.stderr)
        return 1

    hits = 0
    for path in sorted(search_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = path.resolve().relative_to(root)
        for i, line in enumerate(text.splitlines(), start=1):
            if cre.search(line):
                hits += 1
                if args.line_number:
                    print(f"{rel}:{i}:{line}")
                else:
                    print(f"{rel}\t{line}")
    if hits == 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
