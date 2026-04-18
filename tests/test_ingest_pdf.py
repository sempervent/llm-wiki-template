"""Tests for scripts/ingest_pdf.py PDF extraction."""

from __future__ import annotations

from pathlib import Path

import pytest

fitz = pytest.importorskip("fitz")


def test_pages_to_markdown_body_extracts_text(tmp_path: Path) -> None:
    from ingest_pdf import pages_to_markdown_body

    pdf = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello from page one.")
    doc.save(pdf)
    doc.close()

    body = pages_to_markdown_body(pdf)
    assert "## Page 1" in body
    assert "Hello from page one." in body


def test_build_processed_markdown_includes_frontmatter() -> None:
    from ingest_pdf import build_processed_markdown

    md = build_processed_markdown(
        title="My Doc",
        ingested="2026-04-17",
        source_pdf_rel="raw/inbox/x.pdf",
        slug="my-doc",
        body_md="## Page 1\n\ntext\n",
    )
    assert "---" in md
    assert 'source_kind: pdf_extract' in md
    assert 'source_pdf: "raw/inbox/x.pdf"' in md
    assert "id: raw-2026-my-doc" in md
    assert "# My Doc" in md


def test_slugify_stem() -> None:
    from ingest_pdf import slugify_stem

    assert slugify_stem("My File.PDF") == "my-file"
    assert slugify_stem("___") == "document"
