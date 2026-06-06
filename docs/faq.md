# FAQ

Common questions about MCP / tool-using agent security, answered in the context of this dojo.
Terms in **bold** are defined in the [glossary](glossary.md). New here? See the
[recommended path](recommended-path.md).

### What is MCP / tool-using agent security?

It is the practice of keeping an agent safe once it can *take actions* — read files, send email,
issue refunds — and not just produce text. The risk is that untrusted input (tool output,
documents, tool descriptions) can steer those actions. This repo reproduces the common failures
and shows governed alternatives. See the [threat model](threat-model.md).

### How is this different from normal chatbot security?

A chatbot mostly produces text, so the worst case is a bad answer. A tool-using agent can
**execute** consequential actions, so a successful **prompt injection** can exfiltrate data or
trigger a side effect. The mitigations here — policy gates, capability scoping, deterministic
flows, audit traces — exist because text-only guardrails are not enough once actions are
possible.

### What is tool poisoning?

A tool whose *description* looks harmless while its *behavior* is not. An agent that trusts the
description selects the dangerous tool. See
[scenario 02](../scenarios/02_tool_description_poisoning/README.md). The defense is to present
**ChoiceCards** (verified, bounded tool descriptions) and still gate the action with policy.

### Why are raw tool outputs dangerous?

Two reasons. First, they can carry **prompt injection** (instructions hidden in the data) —
[scenario 01](../scenarios/01_prompt_injection_in_tool_result/README.md). Second, they can dump
sensitive data (PII, secrets) straight into context —
[scenario 06](../scenarios/06_raw_tool_output_context_leak/README.md). The **context firewall**
sanitizes, redacts, and bounds tool output before it reaches a decision.

### Why not just expose all tools to the agent?

Exposing every tool grants **ambient authority**: a low-stakes task can reach a high-privilege
action simply because it is in scope. Bounded tool exposure (ChoiceCards) plus **capability
tokens** narrow what a given task can do — least privilege for agents. See
[scenario 05](../scenarios/05_malicious_file_read/README.md).

### Why use deterministic flows instead of letting the model decide?

Known business processes (refunds, escalations, access approval) should be reproducible and
validated. Free-form reasoning can skip steps and reach a side effect without the required
checks. A **deterministic flow** runs the same validated steps every time and surfaces an
explicit approval gate — [scenario 04](../scenarios/04_refund_without_human_approval/README.md).

### How does this relate to enterprise AI governance?

The controls map directly to enterprise requirements: policy-as-code (reviewable rules),
least-privilege execution (capabilities), data minimization (context firewall), process
controls (deterministic flows + approval), and auditability (**audit traces**). The
[consultant playbook](consultant-playbook.md) frames each scenario as a business risk.

### Is this production-ready?

**No.** This is an educational lab and reference architecture. The detectors are deliberately
simple (regex/substring), the tools are simulators, and the data is fake. See the
[security model limitations](security-model.md#limitations).

### Which libraries are used and how?

The dojo is designed around the **Weaver Stack** (AgentFence, agent-kernel/`weaver-kernel`,
contextweaver, ChainWeaver, lessonweaver, VibeGuard, skdr-eval). Currently they are demonstrated
through **local reference implementations** under `src/dojo/integrations/` — the concepts are
real and runnable, but the actual packages are not yet wired in. The
[library map](library-map.md) gives the per-library status, correct install/import names, and
the PyPI name-collision warning for `agentfence`.

### How do I run a scenario and see the result?

```bash
make run-unsafe SCENARIO=01_prompt_injection_in_tool_result
make run-safe   SCENARIO=01_prompt_injection_in_tool_result
```

Governed runs write an **audit trace** to `traces/` (or `DOJO_TRACE_DIR`). Each scenario's
`README.md` shows the exact expected output.
