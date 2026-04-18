#!/usr/bin/env python3
"""
Audit or regenerate wiki/index.md entries from filesystem + frontmatter.

Default mode is --audit (read-only). Use --print-suggestions to emit markdown
list lines you can paste into wiki/index.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from wiki_common import infer_repo_root, load_frontmatter

SECTION_ORDER = [
    ("overview", "Overview"),
    ("entities", "Entities"),
    ("concepts", "Concepts"),
    ("topics", "Topics"),
    ("source-notes", "Source notes"),
    ("analyses", "Analyses"),
    ("comparisons", "Comparisons"),
    ("timelines", "Timelines"),
    ("glossary", "Glossary"),
]

META_SECTION = "## Meta\n\n- [Append-only log](log.md) — Chronological record of ingests, queries, and lint passes.\n"


def discover_pages(wiki_dir: Path) -> dict[str, list[tuple[str, str, Path]]]:
    """Map section key -> list of (title, rel_link, path)."""
    buckets: dict[str, list[tuple[str, str, Path]]] = {k: [] for k, _ in SECTION_ORDER}
    overview_path = wiki_dir / "overview.md"

    for md in sorted(wiki_dir.rglob("*.md")):
        rel = md.relative_to(wiki_dir)
        if rel.name in ("index.md", "log.md"):
            continue
        parts = rel.parts
        if len(parts) == 1 and parts[0] == "overview.md":
            continue  # handled in Overview
        if len(parts) < 2:
            continue
        section = parts[0]
        if section not in buckets:
            continue
        text = md.read_text(encoding="utf-8")
        fm, _ = load_frontmatter(text)
        title = str(fm.get("title") or rel.stem.replace("-", " ").title())
        link_path = rel.as_posix()
        buckets[section].append((title, link_path, md))

    # Overview
    overview_entries: list[tuple[str, str, Path]] = []
    if overview_path.is_file():
        text = overview_path.read_text(encoding="utf-8")
        fm, _ = load_frontmatter(text)
        title = str(fm.get("title") or "Wiki overview")
        overview_entries.append((title, "overview.md", overview_path))

    buckets["overview"] = overview_entries
    return buckets


def render_index(buckets: dict[str, list[tuple[str, str, Path]]]) -> str:
    lines = ["# Wiki index", ""]
    lines.append(
        "First-stop navigation for humans and agents. "
        "Every intentional wiki page should appear here unless it is intentionally transient; "
        "orphans are reported by `scripts/validate_wiki.py`."
    )
    lines.append("")
    for key, heading in SECTION_ORDER:
        lines.append(f"## {heading}")
        lines.append("")
        entries = buckets.get(key, [])
        if not entries:
            lines.append(f"- _(No pages in {key}/ yet.)_")
            lines.append("")
            continue
        for title, link, _p in sorted(entries, key=lambda x: x[0].lower()):
            lines.append(f"- [{title}]({link}) — _description pending_")
        lines.append("")
    lines.append(META_SECTION.rstrip())
    lines.append("")
    return "\n".join(lines)


def read_index_links(index_text: str) -> set[str]:
    """Return set of link targets as in index (relative to wiki/)."""
    from wiki_common import extract_markdown_links, normalize_link_target

    out: set[str] = set()
    for _, target in extract_markdown_links(index_text):
        norm = normalize_link_target(target)
        if norm:
            out.add(norm.replace("\\", "/"))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit or rebuild wiki/index.md")
    parser.add_argument("--root", type=Path, default=None, help="Repo root")
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Compare index.md links to markdown files on disk (default).",
    )
    parser.add_argument(
        "--print-suggestions",
        action="store_true",
        help="Print a full generated index for review (does not write).",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Overwrite wiki/index.md with generated content (use with care).",
    )
    args = parser.parse_args()
    root = infer_repo_root(args.root)
    wiki_dir = root / "wiki"
    if not wiki_dir.is_dir():
        print("ERROR: wiki/ not found", file=sys.stderr)
        return 1

    buckets = discover_pages(wiki_dir)

    if args.write:
        text = render_index(buckets)
        (wiki_dir / "index.md").write_text(text, encoding="utf-8")
        print(f"Wrote {wiki_dir / 'index.md'}")
        return 0

    if args.print_suggestions:
        print(render_index(buckets))
        return 0

    # Audit (default)
    index_path = wiki_dir / "index.md"
    index_text = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
    linked = read_index_links(index_text)

    all_files: set[str] = set()
    for md in wiki_dir.rglob("*.md"):
        rel = md.relative_to(wiki_dir)
        if rel.name in ("index.md", "log.md"):
            continue
        all_files.add(rel.as_posix())

    missing_in_index = sorted(all_files - linked)
    extra_in_index = sorted(linked - all_files - {"log.md"})

    if missing_in_index:
        print("Missing from index (file exists, no link):", file=sys.stderr)
        for m in missing_in_index:
            print(f"  - {m}", file=sys.stderr)
    if extra_in_index:
        print("Index links with no file:", file=sys.stderr)
        for m in extra_in_index:
            print(f"  - {m}", file=sys.stderr)
    if not missing_in_index and not extra_in_index:
        print("Index audit: OK (all wiki pages linked, no dangling index targets).")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
