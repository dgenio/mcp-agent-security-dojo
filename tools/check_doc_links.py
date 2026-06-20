#!/usr/bin/env python3
"""Offline checker for repo-relative Markdown links.

The repository is documentation-led: ``README.md``, the ``docs/`` set, each
``scenarios/NN_*/README.md`` and ``llms.txt`` cross-link heavily and also point
at ``policies/``, ``traces/`` and ``src/`` paths. A renamed file silently breaks
that navigation. This script walks every tracked Markdown file, resolves each
**repo-relative** inline link target against the filesystem, and exits non-zero
if any target is missing.

It is intentionally hermetic: external links (``http(s)://``, ``mailto:``) and
pure in-page anchors (``#fragment``) are skipped, so the check is fast and makes
no network calls — matching the lab's local-only ethos (#79).

Run it directly or via ``make linkcheck``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Inline Markdown links: [text](target). Reference-style and autolinks are not
# used in this repo's docs, so the inline form is sufficient.
_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# Directories that never contain source-controlled docs to validate.
_SKIP_DIRS = {".git", "site", "__pycache__", ".ruff_cache", ".mypy_cache", ".pytest_cache"}


def _iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in _SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        yield path
    llms = root / "llms.txt"
    if llms.exists():
        yield llms


def _is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "tel:", "//"))


def _check_file(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for match in _LINK_RE.finditer(text):
        target = match.group(1).strip()
        # Strip an optional title: [t](url "title").
        target = target.split(" ", 1)[0].strip()
        if not target or target.startswith("#") or _is_external(target):
            continue
        # Drop any in-page anchor or query before resolving the path.
        path_part = target.split("#", 1)[0].split("?", 1)[0]
        if not path_part:
            continue
        resolved = (path.parent / path_part).resolve()
        if not resolved.exists():
            rel = path.relative_to(root)
            errors.append(f"{rel}: broken link -> {target}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    for md in _iter_markdown(root):
        errors.extend(_check_file(md, root))
    if errors:
        print("Broken repo-relative Markdown links found:\n")
        for err in errors:
            print(f"  {err}")
        print(f"\n{len(errors)} broken link(s).")
        return 1
    print("All repo-relative Markdown links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
