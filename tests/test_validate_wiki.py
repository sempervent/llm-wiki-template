"""Smoke tests for validate_wiki.py against this repository."""

import subprocess
import sys
from pathlib import Path


def test_validate_wiki_strict_passes(repo_root: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "validate_wiki.py"), "--strict"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_validate_wiki_detects_broken_link(tmp_path: Path) -> None:
    root = tmp_path
    (root / "wiki").mkdir(parents=True)
    (root / "raw").mkdir(parents=True)
    (root / "AGENTS.md").write_text("# A\n", encoding="utf-8")
    (root / "README.md").write_text("# R\n", encoding="utf-8")
    (root / "LICENSE").write_text("BSD\n", encoding="utf-8")
    (root / "mkdocs.yml").write_text("site_name: t\n", encoding="utf-8")
    (root / "raw" / "README.md").write_text("# raw\n", encoding="utf-8")
    (root / "wiki" / "overview.md").write_text(
        "---\ntitle: O\npage_type: overview\n---\n# O\n", encoding="utf-8"
    )
    (root / "wiki" / "index.md").write_text(
        "# I\n\n## Overview\n\n- [O](overview.md) — x\n", encoding="utf-8"
    )
    (root / "wiki" / "log.md").write_text(
        "# L\n\n## [2026-01-01] lint | x\n\nok\n", encoding="utf-8"
    )
    (root / "wiki" / "entities").mkdir()
    (root / "wiki" / "broken.md").write_text(
        "---\ntitle: B\npage_type: concept\n---\n[bad](entities/file-does-not-exist.md)\n",
        encoding="utf-8",
    )
    (root / "wiki" / "index.md").write_text(
        "# I\n\n## Concepts\n\n- [B](broken.md) — x\n\n## Overview\n\n- [O](overview.md) — x\n",
        encoding="utf-8",
    )
    scripts = Path(__file__).resolve().parent.parent / "scripts"
    proc = subprocess.run(
        [sys.executable, str(scripts / "validate_wiki.py")],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert "Broken link" in proc.stderr
