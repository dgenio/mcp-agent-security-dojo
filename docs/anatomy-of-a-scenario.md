# Anatomy of a scenario

[CONTRIBUTING.md](../CONTRIBUTING.md) explains *which files* a scenario needs;
this doc explains *how a scenario actually runs* end to end across both agents,
the simulated tools, the policy, and the audit trace. Read it once and the
mental model for writing a correct new scenario falls out.

We trace **scenario 03 — unapproved email send**
([walkthrough](../scenarios/03_unapproved_email_send/README.md)) through both
paths. The same request hits the same tools; only the mediation differs.

## The shared shape

Every scenario is two callables over the same simulated tools under
[`src/dojo/tools/`](../src/dojo/tools/):

- `run_unsafe_scenario(scenario, repo_root)` — [`src/dojo/agents/unsafe_agent.py`](../src/dojo/agents/unsafe_agent.py)
- `run_governed_scenario(scenario, repo_root)` — [`src/dojo/agents/governed_agent.py`](../src/dojo/agents/governed_agent.py)

The scenario id (`03_unapproved_email_send`) is the key both agents and
[`tests/test_scenarios.py`](../tests/test_scenarios.py) agree on.

## Unsafe path: how the tool is chosen

The unsafe agent is a real catalog → select → execute → raw-context loop (it has
no per-scenario outcome branches, only per-scenario *configuration*):

1. **Configuration.** `_build_tasks()` maps `03_unapproved_email_send` to a
   `ScenarioTask` with the request *"Reply to the customer about their open
   case."* and no seeded untrusted calls.
2. **Context assembly.** `run_unsafe_scenario` builds context from the effective
   system prompt (with the unreviewed "trust the ticket notes" lesson pasted in),
   the **full** tool catalog (`catalog_prompt()`), and the request — no bounding.
3. **Selection.** `select_tool(...)` is the deterministic stand-in for an LLM.
   For this request the *"reply / respond"* branch fires and returns
   `email.send_reply` addressed to `customer@example.com`.
4. **Execution.** `email.send_reply` is side-effecting, so the send just happens:
   it is recorded in the `SideEffectLedger` with **no policy gate, no approval,
   no decision record**. The step is also "logged" by `InadequateLog.handled()`
   — a useless `"INFO: handled request"` line.
5. **Result.** `status: "risky"`, `approval_record: None`, and a `weak_log` that
   omits everything an audit needs (actor, resource, rationale, args, timestamp).

## Governed path: how the control intervenes

The governed agent routes the same intent through controls and **derives** the
status from the control outcome:

1. `AgentFenceAdapter(_engine(root))` loads
   [`policies/default_policy.yaml`](../policies/default_policy.yaml).
2. `fence.enforce("email.send", "external_customer")` →
   `PolicyEngine.decide(...)` matches the `email.send / external_customer` rule
   with effect **`ask`**.
3. The decision is recorded:
   `trace.add_decision("email.send", "external_customer", "ask", reason)`.
4. Because the effect is not `allow`, the action is downgraded —
   `email.draft_email(...)` instead of `email.send_email(...)` — so the side
   effect never fires unapproved.
5. `trace.add_action("email", result)` records the drafted email and
   `write_trace(trace)` persists the JSON trace (honouring `DOJO_TRACE_DIR`).
6. `_status_from_effect("ask")` yields the reported status
   **`approval_required`**.

## Why "derive the status" matters

The governed status is never hard-coded — it is computed from the real policy
effect (`_status_from_effect`) or the capability / flow / scan / redaction
result. That is why `tests/test_scenarios.py` can bind each scenario to an
expected outcome: a regression in any branch's status derivation is caught. When
you add a scenario, **derive** its status the same way; do not return a literal.

## Where to look next

- [Architecture](architecture.md) — the full governed pipeline and module map.
- [Security model](security-model.md) — what each control guarantees and where it stops.
- [CONTRIBUTING.md → Adding a new scenario](../CONTRIBUTING.md) — the file-by-file checklist.
