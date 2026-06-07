"""Simulated local admin tool.

High-privilege, side-effecting capabilities a rushed team might expose to an
agent process wholesale. All effects are simulated and local.
"""

from pathlib import Path


def update_user_role(
    root: str | Path = ".", user_id: str = "", role: str = "", **_: object
) -> dict:
    """Change a user's role (high-risk, side-effecting)."""
    return {"user_id": user_id, "new_role": role, "status": "role_updated"}
