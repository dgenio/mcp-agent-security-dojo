"""Deterministic customer reply flow."""


def build_customer_reply(customer_name: str, body: str) -> str:
    return f"Hi {customer_name},\n\n{body}\n\n- Support Team"
