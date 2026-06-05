"""Simulated local CRM tool."""

def get_customer_record(customer_id: str) -> dict:
    return {
        "customer_id": customer_id,
        "name": "Pat Example",
        "email": "pat@example.com",
        "status": "gold",
        "notes": "Customer asked about a billing error.",
    }
