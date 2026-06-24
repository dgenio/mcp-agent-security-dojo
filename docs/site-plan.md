# Documentation site plan

This repository's documentation is plain Markdown under `docs/`, readable
directly on GitHub. This page describes the (lightweight) plan for also
publishing it as a browsable site with [MkDocs](https://www.mkdocs.org/) and the
[Material](https://squidfunk.github.io/mkdocs-material/) theme.

The goal is **discoverability without duplication**: the same Markdown files are
the single source of truth, and the site is a thin presentation layer over them.

## What is configured

- **`mkdocs.yml`** at the repo root defines the site name/description, the
  Material theme, a navigation tree over the existing docs, and the
  `superfences` extension so the Mermaid diagrams in the docs (e.g.
  `architecture.md`) render.
- **`docs/index.md`** is the landing page (the GitHub README stays the canonical
  entry point for the repo itself).
- The `docs` optional-dependency group in `pyproject.toml` declares `mkdocs` and
  `mkdocs-material` with minimum-version constraints (`>=`).
- The generated `site/` directory is already gitignored.

## Building locally

```bash
pip install -e .[docs]     # or: make docs-deps
make docs                  # mkdocs build  -> ./site
make docs-serve            # mkdocs serve  -> http://127.0.0.1:8000
```

## Publishing (GitHub Pages) — implemented

The publish step is wired in `.github/workflows/docs.yml`:

1. On every pull request and push, a `check` job installs `.[dev,docs]`,
   verifies repo-relative Markdown links (`make linkcheck`), and builds the site
   (`make docs`) so a broken doc never merges.
2. On push to `main`, a `deploy` job runs `mkdocs gh-deploy --force` with a
   minimal `contents: write` token, publishing the built site to the `gh-pages`
   branch.
3. `site_url` in `mkdocs.yml` matches the published URL
   (`https://dgenio.github.io/mcp-agent-security-dojo/`).

**One-time maintainer step:** enable GitHub Pages for the repository
(Settings → Pages → Deploy from a branch → `gh-pages`) so the published site is
served. Until that toggle is set, the `deploy` job still updates the `gh-pages`
branch, but the site will not be reachable.

## Conventions

- Every new doc added under `docs/` should be linked from `mkdocs.yml`'s `nav`
  and, where relevant, from the README Documentation index.
- Keep relative links working both on GitHub and in the built site (use paths
  relative to the file, not absolute repo paths).
- Preserve the honest "not production-ready" framing on the landing page.
