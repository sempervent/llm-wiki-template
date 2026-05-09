"""Tests for scripts/ingest_pandoc.py (pandoc-based office/PDF ingest)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


def test_strip_leading_atx_heading() -> None:
    from ingest_pandoc import strip_leading_atx_heading

    assert strip_leading_atx_heading("# Title\n\nBody") == "Body"
    assert strip_leading_atx_heading("\n\n# Title\n\nBody") == "Body"
    assert strip_leading_atx_heading("## Section\n\nok") == "## Section\n\nok"


def test_build_processed_markdown() -> None:
    from ingest_pandoc import build_processed_markdown

    md = build_processed_markdown(
        title="My Doc",
        ingested="2026-05-09",
        source_rel="raw/inbox/x.docx",
        slug="my-doc",
        body_md="Hello\n",
        source_format="docx",
        extract_media_dir="my-doc_media",
        pandoc_version="pandoc 3.0",
    )
    assert "source_kind: pandoc_extract" in md
    assert 'source_file: "raw/inbox/x.docx"' in md
    assert "extract_media: \"my-doc_media\"" in md
    assert "id: raw-2026-my-doc" in md
    assert "# My Doc" in md


def test_main_requires_pandoc(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from ingest_pandoc import main

    (tmp_path / "AGENTS.md").write_text("x", encoding="utf-8")
    doc = tmp_path / "raw" / "inbox" / "a.docx"
    doc.parent.mkdir(parents=True)
    doc.write_bytes(b"x")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("ingest_pandoc.pandoc_on_path", lambda: None)
    monkeypatch.setattr(sys, "argv", ["ingest_pandoc.py", str(doc)])
    assert main() == 1


def test_main_writes_frontmatter(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from ingest_pandoc import main

    (tmp_path / "AGENTS.md").write_text("x", encoding="utf-8")
    doc = tmp_path / "raw" / "inbox" / "sample.docx"
    doc.parent.mkdir(parents=True)
    doc.write_bytes(b"x")

    def fake_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        o = cmd.index("-o") + 1
        outp = Path(cmd[o])
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text("# Ignored title\n\nConverted **body**.\n", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("ingest_pandoc.pandoc_on_path", lambda: "/bin/pandoc")
    monkeypatch.setattr("ingest_pandoc.pandoc_version_line", lambda: "pandoc 3.0")
    monkeypatch.setattr("subprocess.run", fake_run)
    monkeypatch.setattr(sys, "argv", ["ingest_pandoc.py", str(doc), "--ingested", "2026-05-09"])
    assert main() == 0

    out = tmp_path / "raw" / "processed" / "2026" / "sample.md"
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "source_kind: pandoc_extract" in text
    assert "Converted **body**." in text


def test_suffix_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from ingest_pandoc import main

    (tmp_path / "AGENTS.md").write_text("x", encoding="utf-8")
    doc = tmp_path / "raw" / "inbox" / "a.xyz"
    doc.parent.mkdir(parents=True)
    doc.write_bytes(b"x")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("ingest_pandoc.pandoc_on_path", lambda: "/bin/pandoc")
    monkeypatch.setattr(sys, "argv", ["ingest_pandoc.py", str(doc)])
    assert main() == 1
