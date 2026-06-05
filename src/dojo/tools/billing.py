"""Simulated local billing tool."""

def get_invoice(invoice_id: str) -> dict:
    return {
        "invoice_id": invoice_id,
        "amount": 350,
        "currency": "USD",
        "paid": True,
        "customer_id": "cust-100",
    }


def issue_refund(invoice_id: str, amount: int) -> dict:
    return {"invoice_id": invoice_id, "amount": amount, "status": "refunded"}
