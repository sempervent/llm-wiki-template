#!/usr/bin/env python3
"""
Extract text from PDF files into markdown under raw/processed/<year>/.

Does not modify existing processed files; writes a new .md path. Pair with
wiki source-notes and append-only log per docs/workflows/ingest.md.
"""

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

try:
    import fitz  # PyMuPDF
except ImportError as e:  # pragma: no cover - exercised when dependency missing
    print("ERROR: PyMuPDF is required. Install with: uv sync", file=sys.stderr)
    raise SystemExit(1) from e


def slugify_stem(name: str) -> str:
    stem = Path(name).stem
    s = stem.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "document"


def yaml_escape_double_quoted(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def pages_to_markdown_body(pdf_path: Path) -> str:
    """Return markdown body with per-page sections (## Page N)."""
    doc = fitz.open(pdf_path)
    try:
        parts: list[str] = []
        for i, page in enumerate(doc):
            text = (page.get_text("text") or "").strip()
            header = f"## Page {i + 1}"
            if not text:
                parts.append(f"{header}\n\n_(No extractable text on this page.)_\n")
            else:
                parts.append(f"{header}\n\n{text}\n")
        return "\n".join(parts)
    finally:
        doc.close()


def build_processed_markdown(
    *,
    title: str,
    ingested: str,
    source_pdf_rel: str,
    slug: str,
    body_md: str,
) -> str:
    yaml_title = yaml_escape_double_quoted(title)
    year = ingested.split("-", 1)[0]
    doc_id = f"raw-{year}-{slug}"
    fm = (
        "---\n"
        f'id: {doc_id}\n'
        f'title: "{yaml_title}"\n'
        f"ingested: {ingested}\n"
        "source_kind: pdf_extract\n"
        f'source_pdf: "{yaml_escape_double_quoted(source_pdf_rel)}"\n'
        "---\n\n"
    )
    h1 = f"# {title}\n\n"
    return fm + h1 + body_md.rstrip() + "\n"


def compute_out_path(root: Path, year: str, slug: str) -> Path:
    return root / "raw" / "processed" / year / f"{slug}.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract PDF text to markdown under raw/processed/<year>/",
    )
    parser.add_argument("pdf", type=Path, help="Path to a .pdf file")
    parser.add_argument("--root", type=Path, default=None, help="Repository root (default: inferred)")
    parser.add_argument(
        "--year",
        default=None,
        help="Subfolder under raw/processed (default: ingested year YYYY)",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="Output filename stem (kebab-case; default: from PDF filename)",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Document title in markdown (default: from slug)",
    )
    parser.add_argument(
        "--ingested",
        default=None,
        help="ISO date YYYY-MM-DD for frontmatter (default: today)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print target path and skip write",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite if output file already exists (default: refuse)",
    )
    args = parser.parse_args()

    pdf_path: Path = args.pdf.resolve()
    if not pdf_path.is_file():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 1
    if pdf_path.suffix.lower() != ".pdf":
        print("ERROR: Input must be a .pdf file", file=sys.stderr)
        return 1

    root = infer_repo_root(args.root)
    try:
        pdf_rel = pdf_path.resolve().relative_to(root)
    except ValueError:
        print(f"ERROR: PDF must live under repository root: {root}", file=sys.stderr)
        return 1

    ingested = args.ingested or date.today().isoformat()
    parts = ingested.split("-")
    if len(parts) != 3 or any(not p.isdigit() for p in parts):
        print("ERROR: --ingested must be YYYY-MM-DD", file=sys.stderr)
        return 1
    year = args.year or parts[0]

    slug = args.slug or slugify_stem(pdf_path.name)
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", slug):
        print(
            "ERROR: slug must be kebab-case (lowercase letters, digits, hyphens). "
            f"Got: {slug!r}",
            file=sys.stderr,
        )
        return 1

    title = args.title or slug.replace("-", " ").title()
    out_path = compute_out_path(root, year, slug)
    source_pdf_rel = str(pdf_rel).replace("\\", "/")

    if out_path.exists() and not args.force:
        print(f"ERROR: Output exists (use --force to overwrite): {out_path}", file=sys.stderr)
        return 1

    body = pages_to_markdown_body(pdf_path)
    text = build_processed_markdown(
        title=title,
        ingested=ingested,
        source_pdf_rel=source_pdf_rel,
        slug=slug,
        body_md=body,
    )

    print(f"Source: {pdf_path}")
    print(f"Output: {out_path}")
    if args.dry_run:
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote {out_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
