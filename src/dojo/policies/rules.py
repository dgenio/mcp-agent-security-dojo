"""Policy data types."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    effect: str
    reason: str


@dataclass(frozen=True)
class PolicyRule:
    action: str
    resource: str
    effect: str
    reason: str
