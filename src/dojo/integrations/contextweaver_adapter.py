"""contextweaver adapter.

TODO: Use real contextweaver ChoiceCards and context firewall APIs when available.
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
