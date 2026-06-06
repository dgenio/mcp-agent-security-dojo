"""contextweaver adapter.

LOCAL REFERENCE IMPLEMENTATION — this is NOT the real library. The real
``contextweaver`` (``pip install contextweaver``) provides ``make_choice_cards``,
``ContextManager``, and redaction hooks that the dojo reimplements locally. See
``docs/library-map.md``.

TODO: Use the real contextweaver ChoiceCards/firewall APIs (tracked in #22).
"""

from dojo.context.choice_cards import build_choice_card
from dojo.context.context_firewall import (
    bounded_summary,
    redact_sensitive_fields,
    sanitize_untrusted_text,
)


def to_choice_card(tool_name: str, allowed_actions: list[str], summary: str) -> dict:
    return build_choice_card(tool_name, allowed_actions, summary)


def firewall_text(raw: str) -> str:
    return redact_sensitive_fields(sanitize_untrusted_text(raw))


def firewall_records(records: list[dict]) -> list[dict]:
    return bounded_summary(records)
