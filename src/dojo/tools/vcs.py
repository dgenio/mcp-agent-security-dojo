"""Simulated local version-control tool."""

from pathlib import Path


def merge_pull_request(root: str | Path = ".", diff: str = "", **_: object) -> dict:
    """Merge a pull request (high-risk, side-effecting).

    The unsafe agent merges whatever diff it is handed with no review gate.
    """
    return {"merged": True, "diff_lines": diff.count("\n") + 1 if diff else 0}
