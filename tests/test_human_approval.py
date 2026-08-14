from datetime import datetime, timedelta, timezone

from dojo.agents.governed_agent import run_governed_scenario
from dojo.flows.human_approval import ActionEnvelope, ApprovalManager


def _envelope(**overrides):
    values = {
        "run_id": "run-1",
        "actor": "governed-agent",
        "action": "email.send",
        "target": "external_customer",
        "arguments": {"to": "customer@example.com", "body": "hello"},
        "policy_version": "1",
    }
    values.update(overrides)
    return ActionEnvelope(**values)


def test_approval_binds_to_exact_action_envelope():
    manager = ApprovalManager()
    envelope = _envelope()
    request = manager.create_request(envelope)

    assert request.status == "pending"
    assert request.action_digest == envelope.digest

    resolved = manager.approve(request.request_id, envelope)
    assert resolved.status == "approved"
    assert resolved.reviewer == "simulated-human"


def test_changed_payload_makes_approval_stale():
    manager = ApprovalManager()
    envelope = _envelope()
    request = manager.create_request(envelope)
    changed = _envelope(arguments={"to": "attacker@example.com", "body": "hello"})

    resolved = manager.approve(request.request_id, changed)
    assert resolved.status == "stale"
    assert "changed" in resolved.reason


def test_reject_cancel_and_expire_are_distinct_terminal_outcomes():
    rejected_manager = ApprovalManager()
    rejected = rejected_manager.create_request(_envelope(run_id="run-reject"))
    assert rejected_manager.reject(rejected.request_id).status == "rejected"

    cancelled_manager = ApprovalManager()
    cancelled = cancelled_manager.create_request(_envelope(run_id="run-cancel"))
    assert cancelled_manager.cancel(cancelled.request_id).status == "cancelled"

    now = [datetime(2026, 8, 14, tzinfo=timezone.utc)]
    expiring_manager = ApprovalManager(ttl_seconds=1, clock=lambda: now[0])
    expiring = expiring_manager.create_request(_envelope(run_id="run-expire"))
    now[0] = now[0] + timedelta(seconds=2)
    assert expiring_manager.expire(expiring.request_id).status == "expired"


def test_email_side_effect_requires_explicit_approval(monkeypatch, tmp_path):
    monkeypatch.setenv("DOJO_TRACE_DIR", str(tmp_path))

    pending = run_governed_scenario("03_unapproved_email_send", repo_root=".")
    assert pending["status"] == "approval_required"
    assert pending["approval"]["status"] == "pending"
    assert pending["email"]["mode"] == "draft"

    rejected = run_governed_scenario(
        "03_unapproved_email_send", repo_root=".", approval_verdict="rejected"
    )
    assert rejected["status"] == "blocked"
    assert rejected["approval"]["status"] == "rejected"
    assert rejected["email"]["mode"] == "draft"

    approved = run_governed_scenario(
        "03_unapproved_email_send", repo_root=".", approval_verdict="approved"
    )
    assert approved["status"] == "allowed"
    assert approved["approval"]["status"] == "approved"
    assert approved["email"]["mode"] == "sent"


def test_refund_side_effect_requires_explicit_approval(monkeypatch, tmp_path):
    monkeypatch.setenv("DOJO_TRACE_DIR", str(tmp_path))

    pending = run_governed_scenario("04_refund_without_human_approval", repo_root=".")
    assert pending["status"] == "approval_required"
    assert pending["approval"]["status"] == "pending"
    assert pending["refund"] is None

    approved = run_governed_scenario(
        "04_refund_without_human_approval", repo_root=".", approval_verdict="approved"
    )
    assert approved["status"] == "allowed"
    assert approved["approval"]["status"] == "approved"
    assert approved["refund"]["status"] == "refunded"
