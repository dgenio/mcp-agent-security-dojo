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
  `superfences` extension so the README/architecture Mermaid diagrams render.
- **`docs/index.md`** is the landing page (the GitHub README stays the canonical
  entry point for the repo itself).
- The `docs` optional-dependency group in `pyproject.toml` pins `mkdocs` and
  `mkdocs-material`.
- The generated `site/` directory is already gitignored.

## Building locally

```bash
pip install -e .[docs]     # or: make docs-deps
make docs                  # mkdocs build  -> ./site
make docs-serve            # mkdocs serve  -> http://127.0.0.1:8000
```

## Publishing (GitHub Pages) — proposed

This is the suggested rollout; it is intentionally **not** wired into CI yet so a
maintainer can opt in deliberately:

1. Add a workflow (e.g. `.github/workflows/docs.yml`) that runs on push to
   `main`, installs `.[docs]`, and runs `mkdocs gh-deploy --force` (or builds and
   uploads a Pages artifact). Scope its token to the minimum needed
   (`contents: write` for `gh-deploy`, or `pages: write` + `id-token: write` for
   the Pages deploy action).
2. Enable **GitHub Pages** for the repository (Settings → Pages), sourced from
   the `gh-pages` branch or the Pages action.
3. Confirm `site_url` in `mkdocs.yml` matches the published URL
   (`https://dgenio.github.io/mcp-agent-security-dojo/`).

## Conventions

- Every new doc added under `docs/` should be linked from `mkdocs.yml`'s `nav`
  and, where relevant, from the README Documentation index.
- Keep relative links working both on GitHub and in the built site (use paths
  relative to the file, not absolute repo paths).
- Preserve the honest "not production-ready" framing on the landing page.
