from dojo.policies.engine import PolicyEngine


def test_policy_decisions_are_deterministic():
    engine = PolicyEngine("policies/default_policy.yaml")
    first = engine.decide("email.send", "external_customer")
    second = engine.decide("email.send", "external_customer")
    assert first == second
    assert first.effect == "ask"


def test_strict_policy_high_value_refund_requires_approval():
    engine = PolicyEngine("policies/strict_policy.yaml")
    decision = engine.decide("refund.issue", "high_value")
    assert decision.effect == "ask"
