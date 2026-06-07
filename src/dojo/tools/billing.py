"""Simulated local billing tool."""

from pathlib import Path

from dojo.tools._fixtures import load_json


def get_invoice(invoice_id: str = "inv-100", root: str | Path = ".", **_: object) -> dict:
    invoice = load_json(root, "fake_invoice.json")
    invoice["invoice_id"] = invoice_id
    return invoice


def issue_refund(
    invoice_id: str = "inv-100", amount: int = 350, root: str | Path = ".", **_: object
) -> dict:
    return {"invoice_id": invoice_id, "amount": amount, "status": "refunded"}
