# Wiki log

Append-only chronological record. New entries go at the **bottom**. Heading format is validated by `scripts/validate_wiki.py`.

---

## [2026-04-17] policy | Initialize template wiki

- Seeded `wiki/` with example pages demonstrating taxonomy and linking.
- Established `raw/processed/2026/example-llm-wiki-note.md` as immutable demo source.
- Documented conventions in `AGENTS.md` and `docs/`.

---

## [2026-04-17] ingest | Example LLM Wiki note

- Filed demo raw source at `raw/processed/2026/example-llm-wiki-note.md`.
- Added source-note [`source-notes/example-llm-wiki-note.md`](source-notes/example-llm-wiki-note.md) and linked from [`concepts/llm-wiki-pattern.md`](concepts/llm-wiki-pattern.md).

---

## [2026-04-17] query | What is the LLM Wiki pattern?

- Answer captured in [`analyses/why-synthesis-layer.md`](analyses/why-synthesis-layer.md) with pointers to concepts and comparisons.

---

## [2026-04-17] lint | Template validation pass

- Ran `validate_wiki.py` with `--strict`; fixed index and link set for demo pages.
