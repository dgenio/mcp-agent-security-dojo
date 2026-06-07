"""Simulated local email tool."""

def draft_email(to: str, subject: str, body: str) -> dict:
    return {"mode": "draft", "to": to, "subject": subject, "body": body}


def send_email(to: str, subject: str, body: str) -> dict:
    return {"mode": "sent", "to": to, "subject": subject, "body": body}


def draft_reply(
    root: str = ".", to: str = "", subject: str = "", body: str = "", **_: object
) -> dict:
    """Compose a reply without sending it (no side effect)."""
    return draft_email(to, subject, body)


def send_reply(
    root: str = ".", to: str = "", subject: str = "", body: str = "", **_: object
) -> dict:
    """Send a reply to an external recipient (side-effecting)."""
    return send_email(to, subject, body)
