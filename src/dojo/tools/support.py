"""Simulated local support history tool."""


def get_ticket_history(ticket_id: str) -> dict:
    return {
        "ticket_id": ticket_id,
        "messages": [
            "Customer reports duplicate charge.",
            "Agent requested invoice screenshot.",
        ],
        "sentiment": "frustrated",
    }
