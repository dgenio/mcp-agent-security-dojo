"""AgentFence adapter.

TODO: Replace fallback with real AgentFence integration when package/API is available.
"""

from dojo.policies.engine import PolicyEngine


class AgentFenceAdapter:
    def __init__(self, policy_engine: PolicyEngine) -> None:
        self.policy_engine = policy_engine

    def enforce(self, action: str, resource: str) -> dict:
        decision = self.policy_engine.decide(action, resource)
        return {"effect": decision.effect, "reason": decision.reason}
