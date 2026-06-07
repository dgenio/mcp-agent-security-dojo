"""Simulated local identity/directory tool."""

from pathlib import Path


def lookup_user(root: str | Path = ".", user_id: str = "cust-100", **_: object) -> dict:
    """Look up a directory user record (read-only)."""
    return {
        "user_id": user_id,
        "name": "Pat Example",
        "role": "customer",
        "email": "pat@example.com",
    }
