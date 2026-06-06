"""AgentFence adapter.

LOCAL REFERENCE IMPLEMENTATION — this is NOT the real AgentFence. It wraps the
dojo's own ``PolicyEngine`` to demonstrate the policy-gate concept. The real
AgentFence is a Go module / GitHub Action (``github.com/dgenio/agentfence``) that
gates recorded MCP/tool calls; the PyPI package ``agentfence`` is an unrelated
third-party project and must not be used. See ``docs/library-map.md``.

TODO: Wire the real AgentFence CI gate (tracked in #26).
"""

from dojo.policies.engine import PolicyEngine


class AgentFenceAdapter:
    def __init__(self, policy_engine: PolicyEngine) -> None:
        self.policy_engine = policy_engine

    def enforce(self, action: str, resource: str) -> dict:
        decision = self.policy_engine.decide(action, resource)
        return {"effect": decision.effect, "reason": decision.reason}
