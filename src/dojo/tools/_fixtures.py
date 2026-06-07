"""Helpers for loading fake fixtures from ``examples/``.

All data under ``examples/`` is synthetic. These helpers resolve a fixture
relative to the dojo repo root so the simulated tools can return realistic,
file-backed payloads instead of inline literals.
"""

import json
from pathlib import Path


def load_text(root: str | Path, name: str) -> str:
    return (Path(root) / "examples" / name).read_text(encoding="utf-8")


def load_json(root: str | Path, name: str) -> dict:
    return json.loads(load_text(root, name))
