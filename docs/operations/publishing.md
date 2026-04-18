# Publishing handbook (optional)

GitHub Pages mirrors **`docs/`** only. Live work stays in **`wiki/`** + **`raw/`** (Obsidian).

## What publishes

- `docs/` → MkDocs site
- `wiki/` is **not** auto-exported into the handbook nav

## Local preview

```bash
make docs-build    # output: site/
make docs-serve
```

## CI

- `.github/workflows/ci.yml` — PR/push
- `.github/workflows/docs.yml` — deploy on `main` (or manual)

Enable **Settings → Pages → GitHub Actions**. No `gh-pages` branch required.

**Next:** [`../quickstart.md`](../quickstart.md) or [`validation.md`](validation.md).
