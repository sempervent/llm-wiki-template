#!/usr/bin/env python3
"""
Report Obsidian-style [[wikilinks]] that do not resolve to an existing wiki page
(by frontmatter title, filename stem, or aliases). Optionally rank by frequency.

Portable `.md` links are validated by scripts/validate_wiki.py; this tool focuses
on [[double-bracket]] mentions that might need a new entity/concept page.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from wiki_common import infer_repo_root, load_frontmatter

# ![[embed]] excluded; [[note|alias]] captures note
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]#|]+)(?:\|([^\]]+))?\]\]")


def collect_wiki_identifiers(root: Path) -> set[str]:
    """Lowercased identifiers that count as 'existing' targets."""
    found: set[str] = set()
    wiki = root / "wiki"
    for path in wiki.rglob("*.md"):
        stem = path.stem.lower()
        found.add(stem)
        text = path.read_text(encoding="utf-8")
        fm, _ = load_frontmatter(text)
        title = fm.get("title")
        if isinstance(title, str) and title.strip():
            found.add(title.strip().lower())
        aliases = fm.get("aliases")
        if isinstance(aliases, list):
            for a in aliases:
                if isinstance(a, str) and a.strip():
                    found.add(a.strip().lower())
    return found


def normalize_wikilink_target(raw: str) -> str:
    s = raw.strip()
    if "#" in s:
        s = s.split("#", 1)[0].strip()
    return s.lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze unresolved [[wikilinks]] in wiki/")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    parser.add_argument(
        "--min-count",
        type=int,
        default=1,
        help="Only print targets mentioned at least this many times (default: 1)",
    )
    args = parser.parse_args()
    root = infer_repo_root(args.root)
    wiki = root / "wiki"
    if not wiki.is_dir():
        print("ERROR: wiki/ not found", file=sys.stderr)
        return 1

    known = collect_wiki_identifiers(root)
    counter: Counter[str] = Counter()
    locations: dict[str, list[str]] = {}

    for path in sorted(wiki.rglob("*.md")):
        rel = str(path.resolve().relative_to(root))
        text = path.read_text(encoding="utf-8")
        for m in WIKILINK_RE.finditer(text):
            target = normalize_wikilink_target(m.group(1))
            if not target:
                continue
            if target in known:
                continue
            counter[target] += 1
            locations.setdefault(target, []).append(rel)

    unresolved = [(c, t) for t, c in counter.items() if c >= args.min_count]
    unresolved.sort(key=lambda x: (-x[0], x[1]))
    if not unresolved:
        print("No unresolved [[wikilinks]] (or none present).")
        return 0

    print("Unresolved [[wikilink]] targets (consider new pages or aliases):\n")
    for count, tgt in unresolved:
        locs = locations.get(tgt, [])
        sample = ", ".join(locs[:3])
        if len(locs) > 3:
            sample += f", … (+{len(locs) - 3} more)"
        print(f"- {tgt!r} — {count} mention(s); e.g. {sample}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
