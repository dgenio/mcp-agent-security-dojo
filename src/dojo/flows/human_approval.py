"""In-memory human-approval state machine for the security dojo.

This module is deliberately local and deterministic enough for teaching/tests. Reviewer
identity and timestamps are simulated evidence unless a caller supplies authenticated
values from a real system.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _canonical_digest(action: str, target: str, arguments: dict) -> str:
    payload = {
        "action": action,
        "target": target,
        "arguments": arguments,
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class ActionEnvelope:
    """Security-relevant action identity bound to an approval request."""

    run_id: str
    actor: str
    action: str
    target: str
    arguments: dict
    policy_version: str

    @property
    def digest(self) -> str:
        return _canonical_digest(self.action, self.target, self.arguments)


@dataclass
class ApprovalRequest:
    request_id: str
    run_id: str
    actor: str
    action: str
    target: str
    action_digest: str
    policy_version: str
    created_at: str
    expires_at: str
    status: str = "pending"
    reviewer: str | None = None
    reviewed_at: str | None = None
    reason: str | None = None

    def as_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "run_id": self.run_id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "action_digest": self.action_digest,
            "policy_version": self.policy_version,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "status": self.status,
            "reviewer": self.reviewer,
            "reviewed_at": self.reviewed_at,
            "reason": self.reason,
            "evidence_note": "reviewer identity/time are simulated unless supplied by an authenticated host",
        }


class ApprovalManager:
    """Create and resolve approval requests bound to exact action envelopes."""

    def __init__(
        self,
        *,
        ttl_seconds: int = 300,
        clock: Callable[[], datetime] = _utcnow,
    ) -> None:
        self.ttl_seconds = ttl_seconds
        self.clock = clock
        self._requests: dict[str, ApprovalRequest] = {}

    def create_request(self, envelope: ActionEnvelope) -> ApprovalRequest:
        now = self.clock()
        request = ApprovalRequest(
            request_id=f"apr-{uuid.uuid4().hex}",
            run_id=envelope.run_id,
            actor=envelope.actor,
            action=envelope.action,
            target=envelope.target,
            action_digest=envelope.digest,
            policy_version=envelope.policy_version,
            created_at=now.isoformat(),
            expires_at=(now + timedelta(seconds=self.ttl_seconds)).isoformat(),
        )
        self._requests[request.request_id] = request
        return request

    def _get_pending(self, request_id: str) -> ApprovalRequest:
        try:
            request = self._requests[request_id]
        except KeyError as exc:
            raise KeyError(f"Unknown approval request: {request_id}") from exc
        if request.status != "pending":
            raise ValueError(f"Approval request is already terminal: {request.status}")
        return request

    def _is_expired(self, request: ApprovalRequest) -> bool:
        return self.clock() >= datetime.fromisoformat(request.expires_at)

    def approve(
        self,
        request_id: str,
        envelope: ActionEnvelope,
        *,
        reviewer: str = "simulated-human",
    ) -> ApprovalRequest:
        request = self._get_pending(request_id)
        now = self.clock()
        request.reviewer = reviewer
        request.reviewed_at = now.isoformat()
        if self._is_expired(request):
            request.status = "expired"
            request.reason = "approval request expired before verdict"
        elif envelope.digest != request.action_digest:
            request.status = "stale"
            request.reason = "security-relevant action envelope changed after review request creation"
        elif envelope.run_id != request.run_id or envelope.policy_version != request.policy_version:
            request.status = "stale"
            request.reason = "run or policy binding changed after review request creation"
        else:
            request.status = "approved"
            request.reason = "exact reviewed action envelope approved"
        return request

    def reject(
        self,
        request_id: str,
        *,
        reviewer: str = "simulated-human",
        reason: str = "human reviewer rejected action",
    ) -> ApprovalRequest:
        request = self._get_pending(request_id)
        now = self.clock()
        request.reviewer = reviewer
        request.reviewed_at = now.isoformat()
        if self._is_expired(request):
            request.status = "expired"
            request.reason = "approval request expired before verdict"
        else:
            request.status = "rejected"
            request.reason = reason
        return request

    def cancel(self, request_id: str, *, reason: str = "request cancelled") -> ApprovalRequest:
        request = self._get_pending(request_id)
        request.status = "cancelled"
        request.reason = reason
        request.reviewed_at = self.clock().isoformat()
        return request

    def expire(self, request_id: str) -> ApprovalRequest:
        request = self._get_pending(request_id)
        if not self._is_expired(request):
            raise ValueError("Approval request has not expired")
        request.status = "expired"
        request.reason = "approval request expired"
        request.reviewed_at = self.clock().isoformat()
        return request
