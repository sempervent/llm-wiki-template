#!/usr/bin/env python3
"""
Optional intake report for files under raw/inbox/: list drops and suggested next steps.

Does not move or rename files. Pair with docs/workflows/ingest.md.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from wiki_common import infer_repo_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Report on raw/inbox/ contents")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    args = parser.parse_args()
    root = infer_repo_root(args.root)
    inbox = root / "raw" / "inbox"
    if not inbox.is_dir():
        print(f"ERROR: {inbox} not found (run scripts/bootstrap.py)", file=sys.stderr)
        return 1

    files = sorted(p for p in inbox.iterdir() if p.is_file() and not p.name.startswith("."))
    if not files:
        print(f"{inbox.relative_to(root)}: (empty)")
        print("\nNext: drop sources here, then follow docs/workflows/ingest.md")
        return 0

    print(f"# Intake: {inbox.relative_to(root)}\n")
    for p in files:
        st = p.stat()
        mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"- `{p.name}` — {st.st_size} bytes, mtime {mtime}")
        if p.suffix.lower() == ".pdf":
            print(
                "  - PDF: consider `uv run python scripts/ingest_pdf.py "
                f"{p.relative_to(root)}` then source-notes + log + validate."
            )
    print(
        "\nNext steps (see templates/ingest-checklist.md): triage, file to "
        "`raw/processed/…`, wiki source-notes, index, log, `validate_wiki.py --strict`."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
