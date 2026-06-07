"""Context size / sensitivity metrics.

Quantifies how much raw data is being placed into an agent's context and how
much of it is sensitive, so the cost and leak of dumping raw tool output can be
measured — and the same numbers can be reported for a bounded/redacted context
to give a concrete before/after comparison.
"""

import re

# Markers that indicate sensitive content sitting in the context.
_SENSITIVE_PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),  # email
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN
    re.compile(r"\b(?:\d[ -]?){13,16}\b"),  # PAN / long card number
    re.compile(r"sk_live_[A-Za-z0-9]+"),  # secret key
    re.compile(r"(?i)\b(ssn|api[_-]?key|secret|password|do_not_expose|internal_notes)\b"),
]


def _to_text(context: object) -> str:
    if isinstance(context, str):
        return context
    return str(context)


def context_metrics(context: object, record_count: int = 0) -> dict:
    """Return approximate size and sensitive-field counts for ``context``.

    ``record_count`` is the number of distinct records folded into the context
    (the caller knows this; it cannot be inferred reliably from text).
    """
    text = _to_text(context)
    sensitive = sum(len(pattern.findall(text)) for pattern in _SENSITIVE_PATTERNS)
    return {
        "approx_chars": len(text),
        "approx_tokens": len(text) // 4,  # rough 4-chars-per-token heuristic
        "record_count": record_count,
        "sensitive_field_count": sensitive,
    }
