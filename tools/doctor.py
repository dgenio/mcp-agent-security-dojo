#!/usr/bin/env python3
"""Check the local development environment for the dojo.

Run via ``make doctor`` or directly::

    python tools/doctor.py

Read-only: it inspects the interpreter version and which packages are importable,
prints an actionable ``OK`` / ``FAIL`` / ``WARN`` line per check, and exits
non-zero only when a *required* check fails. It never installs anything.
"""

from __future__ import annotations

import importlib.util
import sys

# Required checks gate the exit code; optional tools only warn.
_MIN_PYTHON = (3, 10)
_OPTIONAL_TOOLS = ("ruff", "pytest", "mypy")


def _has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def required_checks() -> list[tuple[str, bool]]:
    """Return ``(label, ok)`` for each check that gates the exit code."""
    return [
        (f"Python >= {_MIN_PYTHON[0]}.{_MIN_PYTHON[1]}", sys.version_info >= _MIN_PYTHON),
        ("dojo importable (make setup)", _has_module("dojo")),
    ]


def optional_checks() -> list[tuple[str, bool]]:
    """Return ``(tool, available)`` for each optional dev tool."""
    return [(tool, _has_module(tool)) for tool in _OPTIONAL_TOOLS]


def render(required: list[tuple[str, bool]], optional: list[tuple[str, bool]]) -> list[str]:
    """Build the human-readable report lines (pure — no I/O)."""
    lines = [("OK   " if ok else "FAIL ") + label for label, ok in required]
    for tool, ok in optional:
        suffix = " available" if ok else " missing — run: make setup"
        lines.append(("OK   " if ok else "WARN ") + tool + suffix)
    return lines


def passed(required: list[tuple[str, bool]]) -> bool:
    """True when every required check is OK (drives the exit code)."""
    return all(ok for _, ok in required)


def main() -> int:
    required = required_checks()
    optional = optional_checks()
    for line in render(required, optional):
        print(line)
    return 0 if passed(required) else 1


if __name__ == "__main__":
    sys.exit(main())
