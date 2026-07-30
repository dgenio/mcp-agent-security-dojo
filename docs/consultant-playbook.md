# Consultant playbook

This playbook is for using the dojo in a client setting — a security review, an
AI-adoption readiness assessment, a workshop, or a board-level conversation about
agent risk. It frames each scenario in terms of **business value** and gives you
language for the client conversation, not just commands to run.

> Reminder: this is an educational lab with deliberately simple detectors and
> simulated tools. Position it as a way to *reason about* agent risk and the
> shape of the controls, not as a product you are deploying for the client. See
> the [distribution checklist](distribution-checklist.md) before sharing.

## Why this matters to a business

Tool-using agents change the risk model. A chatbot that is wrong produces a bad
sentence; an agent that is wrong can **send an email, issue a refund, read a
file, close a ticket, or merge code**. The blast radius is real-world side
effects, not just text. The dojo makes that concrete: for each failure mode you
can show the unsafe outcome, then show the specific control that contains it.

The recurring business message: *the fix is rarely a "smarter model" — it is
governance around the agent (policy, bounded context, deterministic flows,
capability scoping, and audit).*

## A 45-minute engagement flow

1. **Frame the risk (5 min).** Agents act. Map the client's intended agent
   actions to the eight scenarios below.
2. **Show one failure end to end (10 min).** Pick the scenario closest to their
   use case. Run `make run-unsafe SCENARIO=...`, then `make run-safe
   SCENARIO=...`, and contrast the outcomes.
3. **Inspect the evidence (5 min).** Open the governed run's `traces/*.json` and
   show the decision + action record — this is what an auditor or incident
   responder would need.
4. **Generalise to controls (10 min).** Walk the
   [security model](security-model.md) control layers and the
   [threat model](threat-model.md) boundaries.
5. **Map to their environment (10 min).** Use the table below to translate each
   control into a requirement they can put on a roadmap.
6. **Leave-behind (5 min).** The repo links, the
   [recommended path](recommended-path.md), and a short list of their highest-risk
   agent actions.

## Scenario → business risk → control → client question

| Scenario | Business risk in plain terms | Control demonstrated | Question to ask the client |
|---|---|---|---|
| 01 Prompt injection in tool result | Untrusted content (a document, a ticket) silently redirects the agent into leaking data | Context firewall + policy deny | "What untrusted text reaches your agent, and who can author it?" |
| 02 Tool-description poisoning | A tool's description lies about what it does; the agent trusts it | Verified ChoiceCard + policy deny | "Who controls the tool catalog your agent sees?" |
| 03 Unapproved email send | The agent contacts customers without sign-off | Policy `ask` → draft pending approval | "Which outbound actions need a human in the loop?" |
| 04 Refund without human approval | Money moves on weak evidence, off-process | Deterministic flow + threshold | "Which business processes must be deterministic, not improvised?" |
| 05 Malicious file read | The agent reads files outside its remit | Capability token scoping | "What is the *minimum* each task should be allowed to touch?" |
| 06 Raw tool-output context leak | Full records (incl. PII) pile into the model context | Bounded summary / redaction | "What data minimisation applies before data hits the model?" |
| 07 AI-generated auth-bypass PR | AI-written code quietly weakens a control and passes CI | Diff safety check + reviewed lessons | "How would you catch a security-weakening change in an AI-authored PR?" |
| 08 Privilege escalation via ambient authority | Untrusted ticket text steers the agent toward privileged admin action | Policy denial via `fence.enforce`; per-task capability scoping as future hardening | "Which privileged actions must never be available as ambient authority?" |

## Mapping controls to enterprise requirements

When the client asks "so what do we actually need?", translate the dojo's
control layers into roadmap items:

- **Policy gate (allow / deny / ask)** → a centrally managed, auditable policy
  for agent/tool actions, with human-approval paths for high-risk operations.
- **Capability scoping** → least-privilege, time-bounded grants per task instead
  of one set of ambient credentials.
- **Bounded context / redaction** → data-minimisation and PII-handling controls
  on everything entering the model.
- **Deterministic flows** → known business processes encoded as validated flows,
  not free-form reasoning.
- **Audit trace** → a decision/action record sufficient for incident response and
  compliance.
- **CI diff safety check** → pre-merge gates for AI-generated code that target
  security-relevant patterns.

## Tips for the conversation

- Lead with the **side effect**, not the model. Executives understand "it sent a
  customer an email it shouldn't have" faster than "prompt injection".
- Use the **trace file** as the artefact: it reframes the discussion from "is the
  model safe?" to "can we prove what the agent did and why?".
- Be explicit about what the dojo does **not** do (see the
  [limitations](security-model.md#limitations)) so you build trust rather than
  overselling.
- Close with one concrete next step tied to *their* highest-risk agent action.
