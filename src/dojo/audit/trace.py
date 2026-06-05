"""Audit trace model."""

from dataclasses import dataclass, field


@dataclass
class AuditTrace:
    scenario: str
    decisions: list[dict] = field(default_factory=list)
    actions: list[dict] = field(default_factory=list)

    def add_decision(self, action: str, resource: str, effect: str, reason: str) -> None:
        self.decisions.append(
            {"action": action, "resource": resource, "effect": effect, "reason": reason}
        )

    def add_action(self, name: str, detail: dict) -> None:
        self.actions.append({"name": name, "detail": detail})
