"""Deterministic refund review flow."""

from dojo.tools.billing import get_invoice
from dojo.tools.support import get_ticket_history


def run_refund_review(invoice_id: str, ticket_id: str) -> dict:
    invoice = get_invoice(invoice_id)
    ticket = get_ticket_history(ticket_id)
    score = 0
    if invoice["paid"]:
        score += 1
    if "duplicate charge" in " ".join(ticket["messages"]).lower():
        score += 1
    requires_human_approval = invoice["amount"] >= 200
    return {
        "invoice": invoice,
        "ticket": ticket,
        "evidence_score": score,
        "requires_human_approval": requires_human_approval,
    }
