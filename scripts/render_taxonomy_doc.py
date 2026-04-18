#!/usr/bin/env python3
"""
Generate docs/reference/page-taxonomy.md from AGENTS.md (Page taxonomy table) and templates/.

Run before `mkdocs build` when taxonomy or templates change (see Makefile `docs-build`).
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


def extract_h2_section(text: str, heading: str) -> str | None:
    """Return body of `## heading` through the next `## ` (exclusive) or EOF."""
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    nxt = re.search(r"^## \S", rest, re.MULTILINE)
    if nxt:
        return rest[: nxt.start()].strip()
    return rest.strip()


def list_templates(templates_dir: Path) -> list[str]:
    if not templates_dir.is_dir():
        return []
    return sorted(p.name for p in templates_dir.glob("*.md"))


def render_markdown(*, taxonomy_section: str, template_names: list[str]) -> str:
    lines = [
        "# Page taxonomy (generated)",
        "",
        "This page is produced by `scripts/render_taxonomy_doc.py` from the "
        "**Page taxonomy** section in `AGENTS.md` (repository root) and the `templates/` "
        "directory. **Do not edit by hand**—run:",
        "",
        "```bash",
        "uv sync --all-groups",
        "uv run python scripts/render_taxonomy_doc.py",
        "```",
        "",
        "## Taxonomy (from AGENTS.md)",
        "",
        taxonomy_section if taxonomy_section.strip() else "_Could not extract taxonomy section._",
        "",
        "## Scaffold templates",
        "",
        "Files in `templates/` used by `scripts/scaffold_page.py`:",
        "",
    ]
    for name in template_names:
        lines.append(f"- `{name}` — in repo root under `templates/{name}` (not part of the MkDocs site).")
    if not template_names:
        lines.append("- _(none found)_")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render docs/reference/page-taxonomy.md")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if the file would change (for CI freshness check).",
    )
    args = parser.parse_args()
    root = infer_repo_root(args.root)
    agents = root / "AGENTS.md"
    if not agents.is_file():
        print(f"ERROR: {agents} not found", file=sys.stderr)
        return 1
    agents_text = agents.read_text(encoding="utf-8")
    section = extract_h2_section(agents_text, "Page taxonomy")
    if section is None:
        section = ""
    templates_dir = root / "templates"
    body = render_markdown(taxonomy_section=section, template_names=list_templates(templates_dir))
    out = root / "docs" / "reference" / "page-taxonomy.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.check:
        if out.is_file() and out.read_text(encoding="utf-8") == body:
            return 0
        print(f"ERROR: {out} is stale; run: uv run python scripts/render_taxonomy_doc.py", file=sys.stderr)
        return 1
    out.write_text(body, encoding="utf-8")
    print(f"Wrote {out.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
