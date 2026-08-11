# Flagship strategy: BREAK IT

The Security Dojo has one job in the dgenio lab portfolio: **BREAK IT**.

It should help a skeptical engineer reproduce an agent-security failure, compare reasonable mitigation approaches, inspect evidence, and understand residual risk. It should not try to demonstrate every library in the ecosystem or act as a general-purpose agent platform.

## Primary journey

The default first-run path is intentionally limited to three scenarios:

| Problem | Flagship scenario | Primary real control |
|---|---|---|
| Untrusted context / tool-result injection | `01_prompt_injection_in_tool_result` | `contextweaver` |
| Unauthorized outbound action | `03_unapproved_email_send` | `weaver-kernel` + AgentFence boundary |
| Known high-risk business process | `04_refund_without_human_approval` | `chainweaver` + authorization/policy around the write |

The other scenarios remain useful extended exercises. They are not blockers for first success and must not force unrelated packages into the flagship install.

## Evidence hierarchy

Where feasible, use the same synthetic case for three implementations:

1. **unsafe** — intentionally under-governed and expected to expose the failure mode;
2. **DIY/reference** — a competent local mitigation, clearly labelled as local code;
3. **real** — the actual relevant OSS package or AgentFence sidecar/boundary.

The comparison is not "bad code versus our product." The DIY path is deliberately competent so a reader can judge the maintenance/delegation trade-off honestly.

A generated receipt must identify execution mode and implementation provenance. A requested `real` run must fail if the real component cannot execute; it must never silently fall back to the reference path.

## What counts as strong evidence

A flagship claim should have:

- a reproducible unsafe failure;
- a legitimate safe action that still succeeds;
- a competent DIY/reference mitigation;
- a real-library path when available;
- version or commit provenance for real components;
- adversarial variants beyond the canonical authored string;
- benign near-matches to expose false positives;
- explicit limitations, residual risk, known bypasses, and control-failure behavior.

A perfect all-green attack corpus is not the goal. Known failures are useful evidence when they are reproducible and clearly described.

## Scope guardrails

Before the flagship adoption gates pass, do **not** make these priorities:

- whole-stack installation;
- `skdr-eval`, `lessonweaver`, or VibeGuard integration solely for portfolio completeness;
- hosted playgrounds or a live MCP product;
- leaderboards or LLM judges;
- workshop/content-production machinery;
- GitHub Pages as a growth project;
- taxonomy/compliance mapping as a substitute for evidence;
- adding more scenarios because onboarding or conversion is weak.

## Dependency rule

Each scenario should depend on the smallest authentic component set needed to prove its claim. The Dojo is a composable security lab, not a monolithic Weaver Stack installer.

## Relationship to the other labs

- **Security Dojo — BREAK IT:** reproduce failures and mitigations.
- **agent-routing-eval-lab — MEASURE IT:** evaluate routing changes with `contextweaver` + `skdr-eval` only.
- **enterprise-agent-control-plane — ASSEMBLE IT:** later prove that already-useful controls compose in one reference architecture.

The Control Plane must not be responsible for convincing users that the individual libraries are useful.

## Decision rule

Do not broaden the Dojo because a feature is interesting. Broaden it only when external use reveals a repeated need that belongs specifically in a security failure/mitigation lab.
