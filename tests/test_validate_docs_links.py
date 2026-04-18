"""Tests for validate_docs_links.py."""

import subprocess
import sys
from pathlib import Path


def test_validate_docs_links_passes_on_repo(repo_root: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "validate_docs_links.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_validate_docs_links_detects_broken(tmp_path: Path) -> None:
    scripts = Path(__file__).resolve().parent.parent / "scripts"
    (tmp_path / "docs").mkdir(parents=True)
    (tmp_path / "docs" / "a.md").write_text("[x](missing.md)\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# R\n", encoding="utf-8")
    (tmp_path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (tmp_path / "mkdocs.yml").write_text("site_name: t\n", encoding="utf-8")
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "index.md").write_text("# I\n", encoding="utf-8")
    (tmp_path / "wiki" / "log.md").write_text("# L\n\n## [2026-01-01] lint | x\n\nok\n", encoding="utf-8")
    (tmp_path / "wiki" / "overview.md").write_text("---\ntitle: O\npage_type: overview\n---\n# O\n", encoding="utf-8")
    (tmp_path / "raw").mkdir()
    (tmp_path / "raw" / "README.md").write_text("# r\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(scripts / "validate_docs_links.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert "Broken link" in proc.stderr


def test_render_taxonomy_extract_section() -> None:
    from render_taxonomy_doc import extract_h2_section

    text = "## Foo\n\nhello\n\n## Bar\n\nworld\n"
    assert extract_h2_section(text, "Foo") == "hello"
    assert extract_h2_section(text, "Bar") == "world"
