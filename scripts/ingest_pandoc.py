#!/usr/bin/env python3
"""
Convert PDF, DOCX, or PPTX to markdown under raw/processed/<year>/ using Pandoc.

Writes extracted images next to the markdown (`<slug>_media/`) so Obsidian shows
embedded figures via relative paths. Requires `pandoc` on PATH; PDF input often
needs Poppler installed as well (see docs/workflows/ingest.md).

Does not overwrite existing output unless --force. Pair with wiki source-notes
and append-only log per docs/workflows/ingest.md.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from wiki_common import infer_repo_root, slugify_stem, yaml_escape_double_quoted

ALLOWED_SUFFIXES = {".pdf", ".docx", ".pptx"}

FORMAT_FOR_SUFFIX = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".pptx": "pptx",
}


def pandoc_on_path() -> str | None:
    return shutil.which("pandoc")


def pandoc_version_line() -> str | None:
    exe = pandoc_on_path()
    if not exe:
        return None
    try:
        proc = subprocess.run(
            [exe, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except OSError:
        return None
    if proc.returncode != 0 or not proc.stdout:
        return None
    first = proc.stdout.strip().splitlines()[0].strip()
    return first[:200] if first else None


def strip_leading_atx_heading(body: str) -> str:
    """Remove the first top-level # heading block (common pandoc output)."""
    lines = body.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith("# ") and not lines[i].startswith("## "):
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        return "\n".join(lines[i:])
    return body


def build_processed_markdown(
    *,
    title: str,
    ingested: str,
    source_rel: str,
    slug: str,
    body_md: str,
    source_format: str,
    extract_media_dir: str,
    pandoc_version: str | None,
) -> str:
    yaml_title = yaml_escape_double_quoted(title)
    year = ingested.split("-", 1)[0]
    doc_id = f"raw-{year}-{slug}"
    pv = yaml_escape_double_quoted(pandoc_version or "unknown")
    fm_lines = [
        "---",
        f"id: {doc_id}",
        f'title: "{yaml_title}"',
        f"ingested: {ingested}",
        "source_kind: pandoc_extract",
        f"source_format: {source_format}",
        f'source_file: "{yaml_escape_double_quoted(source_rel)}"',
        f'extract_media: "{yaml_escape_double_quoted(extract_media_dir)}"',
        f'pandoc_version: "{pv}"',
        "---",
        "",
    ]
    fm = "\n".join(fm_lines)
    h1 = f"# {title}\n\n"
    return fm + h1 + body_md.rstrip() + "\n"


def compute_out_path(root: Path, year: str, slug: str) -> Path:
    return root / "raw" / "processed" / year / f"{slug}.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert PDF/DOCX/PPTX to markdown via pandoc (images beside output)",
    )
    parser.add_argument("document", type=Path, help="Path to .pdf, .docx, or .pptx")
    parser.add_argument("--root", type=Path, default=None, help="Repository root (default: inferred)")
    parser.add_argument(
        "--year",
        default=None,
        help="Subfolder under raw/processed (default: ingested year YYYY)",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="Output filename stem (kebab-case; default: from input filename)",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Document title for H1 (default: from slug)",
    )
    parser.add_argument(
        "--ingested",
        default=None,
        help="ISO date YYYY-MM-DD for frontmatter (default: today)",
    )
    parser.add_argument(
        "--keep-doc-heading",
        action="store_true",
        help="Keep pandoc's first # heading (may duplicate the added title)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths and pandoc command; do not write",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output .md and re-use extract dir (default: refuse)",
    )
    parser.add_argument(
        "--extra-arg",
        action="append",
        default=[],
        dest="extra_args",
        help="Extra arguments appended to the pandoc invocation",
    )
    args = parser.parse_args()

    if not pandoc_on_path():
        print(
            "ERROR: pandoc not found on PATH. Install pandoc (e.g. brew install pandoc; "
            "apt install pandoc). PDF conversion often also needs poppler.",
            file=sys.stderr,
        )
        return 1

    doc_path: Path = args.document.resolve()
    if not doc_path.is_file():
        print(f"ERROR: File not found: {doc_path}", file=sys.stderr)
        return 1

    suf = doc_path.suffix.lower()
    if suf not in ALLOWED_SUFFIXES:
        print(f"ERROR: Expected one of {sorted(ALLOWED_SUFFIXES)}; got {suf!r}", file=sys.stderr)
        return 1

    root = infer_repo_root(args.root)
    try:
        source_rel = str(doc_path.resolve().relative_to(root)).replace("\\", "/")
    except ValueError:
        print(f"ERROR: Input must live under repository root: {root}", file=sys.stderr)
        return 1

    ingested = args.ingested or date.today().isoformat()
    parts = ingested.split("-")
    if len(parts) != 3 or any(not p.isdigit() for p in parts):
        print("ERROR: --ingested must be YYYY-MM-DD", file=sys.stderr)
        return 1
    year = args.year or parts[0]

    slug = args.slug or slugify_stem(doc_path.name)
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", slug):
        print(
            f"ERROR: slug must be kebab-case (lowercase letters, digits, hyphens). Got: {slug!r}",
            file=sys.stderr,
        )
        return 1

    title = args.title or slug.replace("-", " ").title()
    out_path = compute_out_path(root, year, slug)
    work_dir = out_path.parent
    media_dir_name = f"{slug}_media"

    media_path = work_dir / media_dir_name

    if out_path.exists() and not args.force:
        print(f"ERROR: Output exists (use --force to overwrite): {out_path}", file=sys.stderr)
        return 1

    if media_path.exists() and not args.force:
        print(
            f"ERROR: Extract media directory exists (use --force to overwrite): {media_path}",
            file=sys.stderr,
        )
        return 1

    if args.force:
        if out_path.exists():
            out_path.unlink()
        if media_path.exists():
            shutil.rmtree(media_path)

    pv_line = pandoc_version_line()
    pandoc_exe = pandoc_on_path() or "pandoc"
    # Absolute paths so inputs can live in raw/inbox/ while output is raw/processed/<year>/.
    cmd = [
        pandoc_exe,
        str(doc_path.resolve()),
        "-o",
        str(out_path.resolve()),
        "-t",
        "markdown",
        "--wrap=none",
        f"--extract-media={media_path}",
    ]
    cmd.extend(args.extra_args)

    print(f"Source: {doc_path}")
    print(f"Working directory: {work_dir}")
    print(f"Output: {out_path}")
    print(f"Media:   {media_path} (created by pandoc)")
    print(f"Pandoc:  {' '.join(cmd)}")
    if args.dry_run:
        return 0

    work_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        cmd,
        cwd=work_dir,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if proc.returncode != 0:
        print("ERROR: pandoc failed", file=sys.stderr)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        if proc.stdout:
            print(proc.stdout, file=sys.stderr)
        if suf == ".pdf":
            print(
                "Hint: PDF→markdown via pandoc requires a Pandoc build with PDF support and "
                "often Poppler. For text-only fallback try: "
                "uv run python scripts/ingest_pdf.py <path>",
                file=sys.stderr,
            )
        return 1

    if not out_path.is_file():
        print(f"ERROR: pandoc did not write expected file: {out_path}", file=sys.stderr)
        return 1

    body_raw = out_path.read_text(encoding="utf-8")
    strip_heading = not args.keep_doc_heading
    body = strip_leading_atx_heading(body_raw) if strip_heading else body_raw.strip()
    text = build_processed_markdown(
        title=title,
        ingested=ingested,
        source_rel=source_rel,
        slug=slug,
        body_md=body,
        source_format=FORMAT_FOR_SUFFIX[suf],
        extract_media_dir=media_dir_name,
        pandoc_version=pv_line,
    )
    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote {out_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
