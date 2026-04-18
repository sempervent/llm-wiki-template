"""Log heading format."""

from wiki_common import LOG_HEADING_PATTERN


def test_log_heading_pattern_accepts_valid() -> None:
    line = "## [2026-04-17] ingest | Example title"
    assert LOG_HEADING_PATTERN.match(line.strip())


def test_log_heading_pattern_rejects_bad_kind() -> None:
    line = "## [2026-04-17] unknown | Nope"
    assert LOG_HEADING_PATTERN.match(line.strip()) is None
