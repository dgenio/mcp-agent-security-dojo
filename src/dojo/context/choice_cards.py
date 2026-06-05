"""Bounded context card builder."""


def build_choice_card(tool_name: str, allowed_actions: list[str], summary: str) -> dict:
    return {
        "tool": tool_name,
        "allowed_actions": allowed_actions,
        "summary": summary,
    }
