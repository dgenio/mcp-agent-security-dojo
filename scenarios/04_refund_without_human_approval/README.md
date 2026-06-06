# Scenario 04 — Refund without human approval

## The attack

A known business process (refund review) is run as a single side-effecting call instead of a
validated, gated flow. The unsafe agent simply issues the refund, skipping evidence checks and
any approval threshold.

**Real-world example:** an agent issues a high-value refund directly from a customer's complaint
text, with no verification of invoice ownership or duplicate-charge evidence.

## Unsafe path

`unsafe_run.py` calls `billing.issue_refund("inv-100", 350)`:

```text
{'status': 'risky',
 'risky_action': {'invoice_id': 'inv-100', 'amount': 350, 'status': 'refunded'}}
```

## Governed path

The governed path runs the **deterministic refund flow**
([`run_refund_review`](../../src/dojo/flows/refund_review.py)), which gathers invoice + ticket
evidence and computes an `evidence_score`. Because the amount (`350`) is at or above the
threshold, `requires_human_approval` is `True`, and the strict policy returns `ask` for
`refund.issue / high_value`:

```text
{'status': 'approval_required',
 'decision': {'effect': 'ask', 'reason': 'High-value refunds require human approval.'},
 'review': {'evidence_score': 2, 'requires_human_approval': True, ...},
 'trace_path': 'traces/04_..._....json'}
```

Committed sample trace:
[`traces/sample_safe_trace_04.json`](../../traces/sample_safe_trace_04.json).

## Control / library mapping

| Control | Module | Reference library |
|---|---|---|
| Deterministic refund flow | `src/dojo/flows/refund_review.py` | ChainWeaver |
| Approval threshold / `ask` | `policies/strict_policy.yaml`, `src/dojo/policies/engine.py` | agent-kernel, AgentFence |

## Run it

```bash
make run-unsafe SCENARIO=04_refund_without_human_approval
make run-safe   SCENARIO=04_refund_without_human_approval
```

## See also

- [Threat model](../../docs/threat-model.md) — boundary: *privileged side effect*.
- [Glossary: deterministic flow](../../docs/glossary.md).
