"""Simulated local email tool."""

def draft_email(to: str, subject: str, body: str) -> dict:
    return {"mode": "draft", "to": to, "subject": subject, "body": body}


def send_email(to: str, subject: str, body: str) -> dict:
    return {"mode": "sent", "to": to, "subject": subject, "body": body}
