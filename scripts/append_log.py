#!/usr/bin/env python3
"""Append a correctly formatted entry to wiki/log.md."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from wiki_common import infer_repo_root

KINDS = ("ingest", "query", "lint", "refactor", "policy")


def main() -> int:
    parser = argparse.ArgumentParser(description="Append an entry to wiki/log.md")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument(
        "--kind",
        required=True,
        choices=KINDS,
        help="Log entry kind",
    )
    parser.add_argument("--title", required=True, help="Short title after the pipe")
    parser.add_argument(
        "--body",
        default=None,
        help="Markdown body (use - for stdin if omitted and pipe content)",
    )
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    args = parser.parse_args()

    when = args.date or date.today().isoformat()
    parts = when.split("-")
    if len(parts) != 3 or any(not p.isdigit() for p in parts):
        print("ERROR: --date must be YYYY-MM-DD", file=sys.stderr)
        return 1

    body_text = args.body
    if body_text is None:
        body_text = sys.stdin.read()
    if not body_text.strip():
        body_text = "- _(No details provided.)_\n"

    root = infer_repo_root(args.root)
    log_path = root / "wiki" / "log.md"
    if not log_path.is_file():
        print(f"ERROR: {log_path} not found", file=sys.stderr)
        return 1

    heading = f"## [{when}] {args.kind} | {args.title.strip()}"
    block = f"\n---\n\n{heading}\n\n{body_text.rstrip()}\n\n"

    existing = log_path.read_text(encoding="utf-8")
    log_path.write_text(existing.rstrip() + block, encoding="utf-8")
    print(f"Appended to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
