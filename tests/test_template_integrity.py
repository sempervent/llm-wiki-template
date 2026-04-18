"""Templates and scaffold inputs exist."""

from pathlib import Path

REQUIRED_TEMPLATES = [
    "source-note.md",
    "entity-page.md",
    "concept-page.md",
    "analysis-page.md",
    "comparison-page.md",
    "timeline-page.md",
    "overview-page.md",
    "glossary-page.md",
    "ingest-checklist.md",
    "lint-checklist.md",
]


def test_all_templates_exist(repo_root: Path) -> None:
    tdir = repo_root / "templates"
    for name in REQUIRED_TEMPLATES:
        p = tdir / name
        assert p.is_file(), f"missing {p}"
        text = p.read_text(encoding="utf-8")
        assert len(text.strip()) > 0


def test_scaffold_templates_have_placeholders(repo_root: Path) -> None:
    for name in [
        "source-note.md",
        "entity-page.md",
        "concept-page.md",
        "analysis-page.md",
        "comparison-page.md",
        "timeline-page.md",
        "overview-page.md",
        "glossary-page.md",
    ]:
        text = (repo_root / "templates" / name).read_text(encoding="utf-8")
        assert "{{TITLE}}" in text
        assert "{{DATE}}" in text
