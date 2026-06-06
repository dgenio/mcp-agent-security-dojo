# Threat model

This threat model defines what the dojo protects, the trust boundaries an agent crosses,
the attacker's assumed capabilities, and a per-scenario mapping from threat to mitigating
control. It is the credibility backbone for the [security model](security-model.md) and the
per-scenario walkthroughs under `scenarios/`.

## Scope and assumptions

- All tools are **local simulators** with fake data (`src/dojo/tools/`); there is no real
  network, no real customer data, and no real side effects.
- The "model" is deterministic and local — these scenarios demonstrate the *mechanism* of
  each failure, not a live LLM. The mitigations are what would matter in a real deployment.
- The defenders are the controls in `src/dojo/` (policy engine, capability tokens, context
  firewall, deterministic flows, audit traces, diff scanner).

## Assets

| Asset | Examples in the dojo |
|---|---|
| Sensitive data | PII (SSN, customer email), `examples/internal_secrets.txt`, full CRM/billing records |
| Side-effecting actions | `email.send_email`, `billing.issue_refund`, file reads |
| Authorization controls | the policy engine and capability tokens themselves (a diff can weaken them) |
| Auditability | the integrity and completeness of `traces/*.json` |

## Trust boundaries

An agent is dangerous precisely because it carries untrusted data across boundaries into a
context that can take actions. The dojo models four:

1. **Untrusted tool output** — text returned by a tool (e.g. `docs.search_docs`) may contain
   injected instructions. Crossing point: tool result → agent context (scenarios 01, 06).
2. **Poisoned tool metadata** — a tool's *description* is attacker-influenced and may not
   match its behavior. Crossing point: tool card → tool selection (scenario 02).
3. **Privileged side effects** — actions that change state or move data (email, refund, file
   read) cross from "decided" to "done". Crossing point: decision → execution (scenarios 03, 04, 05).
4. **AI-generated code** — a generated diff crosses from proposal into the codebase and can
   silently weaken a control. Crossing point: diff → merge (scenario 07).

## Attacker model

The attacker can influence any data that flows into the agent but cannot directly execute
code in the host. Concretely, they can:

- plant instructions inside tool output or documents the agent will read;
- publish a tool whose description is benign but whose behavior is not;
- craft inputs that nudge the agent toward a privileged action;
- propose an AI-generated diff that looks reasonable and passes basic CI.

They cannot bypass the policy engine, forge a capability token, or edit the audit trace
directly — those are the trust anchors the governed path relies on.

## Per-scenario threat table

| # | Threat | Entry point (boundary) | Impact if unmitigated | Mitigating control | Module |
|---|---|---|---|---|---|
| 01 | Prompt injection in tool result | Untrusted tool output | SSN emailed to attacker | Context firewall sanitize/redact + policy deny | `context/context_firewall.py`, `policies/engine.py` |
| 02 | Tool description poisoning | Poisoned tool metadata | Hidden dangerous action executes | Verified ChoiceCard + policy deny | `context/choice_cards.py`, `policies/engine.py` |
| 03 | Unapproved email send | Privileged side effect | Email sent without approval | Policy `ask` → draft pending approval | `policies/engine.py`, `tools/email.py` |
| 04 | Refund without human approval | Privileged side effect | $350 refund on weak evidence | Deterministic flow + approval threshold | `flows/refund_review.py`, `policies/strict_policy.yaml` |
| 05 | Malicious file read | Privileged side effect | Secrets file read | Capability token path scoping | `integrations/agent_kernel_adapter.py` |
| 06 | Raw tool output context leak | Untrusted tool output | Full PII dumped into context | Bounded summary (allow-list of fields) | `context/context_firewall.py` |
| 07 | AI-generated auth bypass PR | AI-generated code | Auth-weakening diff merges | Diff safety scan blocks on findings | `integrations/vibeguard_adapter.py` |

## Residual risks and out of scope

- **Detector completeness.** The injection and diff detectors are regex/substring based and
  are best-effort by design — they will miss novel phrasings. See
  [security model: limitations](security-model.md#limitations). Realistic-detector upgrades
  are tracked in #32 and #38.
- **Defense-in-depth gaps.** Some scenarios currently demonstrate a single control rather
  than the full layered pipeline; broadening coverage is tracked across the governed-path
  issues (e.g. #42, #43, #52).
- **Out of scope:** live network/LLM threats, host compromise, supply-chain attacks on the
  Python toolchain, and multi-tenant isolation. These are not modeled by the local simulators.
