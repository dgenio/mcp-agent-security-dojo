"""Simulated local CRM tool."""

from pathlib import Path

from dojo.tools._fixtures import load_json


def search_customer(root: str | Path = ".", query: str = "", **_: object) -> list[dict]:
    """Return matching customer stubs (id + name only)."""
    profile = get_customer_profile(root)
    return [{"customer_id": profile["customer_id"], "name": profile["name"]}]


def get_customer_profile(root: str | Path = ".", **_: object) -> dict:
    """Return the full customer profile, including PII and internal-only notes.

    Mirrors a real enterprise CRM record: routine fields sit right next to
    sensitive PII and an internal fraud note that must never reach the customer.
    """
    return load_json(root, "fake_customer_case.json")
