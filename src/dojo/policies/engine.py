"""Simple deterministic policy engine."""

from pathlib import Path

import yaml

from dojo.policies.rules import PolicyDecision, PolicyRule


class PolicyEngine:
    def __init__(self, policy_path: str) -> None:
        data = yaml.safe_load(Path(policy_path).read_text(encoding="utf-8"))
        self.rules = [
            PolicyRule(
                action=str(item["action"]),
                resource=str(item["resource"]),
                effect=str(item["effect"]),
                reason=str(item.get("reason", "policy rule match")),
            )
            for item in data.get("rules", [])
        ]

    def decide(self, action: str, resource: str) -> PolicyDecision:
        for rule in self.rules:
            if rule.action in (action, "*") and rule.resource in (resource, "*"):
                return PolicyDecision(effect=rule.effect, reason=rule.reason)
        return PolicyDecision(effect="deny", reason="default deny")
