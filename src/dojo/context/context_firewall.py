"""Untrusted context handling and redaction."""

import re

_PROMPT_INJECTION_PATTERNS = [r"ignore all previous instructions", r"send .* to attacker"]
# Local part is optional (``*``) so a bare or bracket-prefixed address such as the
# ``@evil.test`` left behind after injection sanitization is still redacted. A dotted
# domain is required to avoid matching stray ``@`` characters.
_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def sanitize_untrusted_text(raw: str) -> str:
    cleaned = raw
    for pattern in _PROMPT_INJECTION_PATTERNS:
        cleaned = re.sub(pattern, "[blocked-instruction]", cleaned, flags=re.IGNORECASE)
    return cleaned


def redact_sensitive_fields(raw: str) -> str:
    return _EMAIL_PATTERN.sub("[redacted-email]", raw)


def bounded_summary(records: list[dict]) -> list[dict]:
    allowed_fields = {"ticket_id", "invoice_id", "status", "sentiment"}
    summaries = []
    for item in records:
        summaries.append({k: v for k, v in item.items() if k in allowed_fields})
    return summaries
