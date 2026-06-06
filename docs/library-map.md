# Library map

This dojo is designed around the **Weaver Stack** — a set of agent-governance libraries.
Today the governed path demonstrates their *concepts* through **local reference
implementations** under `src/dojo/integrations/`; the real packages are **not yet wired in**
(`pyproject.toml` declares only `pyyaml`). This page is deliberately honest about that gap so
that anyone reading or demoing the repo is not misled. Real integration is tracked in
[#19](https://github.com/dgenio/mcp-agent-security-dojo/issues/19) and its child issues.

## Status at a glance

| README name | Real repo | Language | Install (dist name) | Import name | Provides | Dojo status |
|---|---|---|---|---|---|---|
| AgentFence | [dgenio/agentfence](https://github.com/dgenio/agentfence) | **Go** (module `github.com/dgenio/agentfence`, ships `action.yml`) | n/a — **not a pip package** | n/a | Policy gate over *recorded* MCP/tool calls (decision/redaction/approval/audit); GitHub Action | Stub (local `PolicyEngine` wrapper) |
| agent-kernel | [dgenio/agent-kernel](https://github.com/dgenio/agent-kernel) | Python | `pip install weaver-kernel` | `weaver_kernel` | `PolicyEngine`, `CapabilityToken`, `HMACTokenProvider`, `Firewall`, `BudgetManager`, `TraceStore` | Stub (hand-rolled `CapabilityToken`) |
| contextweaver | [dgenio/contextweaver](https://github.com/dgenio/contextweaver) | Python | `pip install contextweaver` | `contextweaver` | `make_choice_cards`, `render_cards_text`, `ContextManager`, redaction hooks, budgets | Stub (local choice cards + firewall) |
| ChainWeaver | [dgenio/ChainWeaver](https://github.com/dgenio/ChainWeaver) | Python | `pip install chainweaver` (`chainweaver[yaml]`) | `chainweaver` | `FlowBuilder`, `@tool`, executor, schema validation, decisions/cost/lessons | Stub (fold-over-steps) |
| lessonweaver | [dgenio/lessonweaver](https://github.com/dgenio/lessonweaver) | Python | **not on PyPI** — `pip install git+https://github.com/dgenio/lessonweaver.git` | `lessonweaver` | `LessonDetector`, governance promotion, trace ingestion, registry | Stub (static list) |
| VibeGuard | [dgenio/vibeguard](https://github.com/dgenio/vibeguard) | Python | `pip install vibeguard-gate` | `vibeguard` | Real diff scanner + Dockerfile + CI gate | Stub (3-substring scan) |
| skdr-eval | (offline policy/routing evaluation) | Python | — | — | Replay a candidate policy/router change against historical traces; emit a decision report | Not represented yet (#39, #49) |

> ⚠️ **PyPI name collision:** the PyPI package named `agentfence` is an **unrelated
> third-party project** (author "Haggai Shachar", `agentfence.ai`). Do **not** add it as a
> dependency. The AgentFence used here is the Go module / GitHub Action above.

## Per-library value proposition

- **AgentFence — local MCP/tool policy enforcement.** Problem it solves: recorded tool/MCP
  calls can violate policy with no gate. Role in the dojo: the policy `allow`/`deny`/`ask`
  decision and (eventually) a CI gate over a JSONL of tool calls. Demonstrated by:
  scenarios [01](../scenarios/01_prompt_injection_in_tool_result/README.md),
  [02](../scenarios/02_tool_description_poisoning/README.md),
  [03](../scenarios/03_unapproved_email_send/README.md).
  Local reference: `src/dojo/integrations/agentfence_adapter.py` (wraps `policies/engine.py`).
- **agent-kernel (`weaver-kernel`) — capability-scoped execution and audit.** Problem:
  one set of credentials grants ambient authority to every action. Role: capability tokens that
  narrow what a task may do, plus the audit trace primitives. Demonstrated by:
  scenario [05](../scenarios/05_malicious_file_read/README.md). Local reference:
  `src/dojo/integrations/agent_kernel_adapter.py`, `src/dojo/audit/`.
- **contextweaver — bounded context and ChoiceCards.** Problem: raw tool output and full tool
  catalogs overload and poison the model context. Role: ChoiceCards (bounded tool selection),
  redaction, and bounded summaries. Demonstrated by:
  scenarios [01](../scenarios/01_prompt_injection_in_tool_result/README.md),
  [02](../scenarios/02_tool_description_poisoning/README.md),
  [06](../scenarios/06_raw_tool_output_context_leak/README.md). Local reference:
  `src/dojo/integrations/contextweaver_adapter.py`, `src/dojo/context/`.
- **ChainWeaver (`chainweaver`) — deterministic, schema-validated flows.** Problem: known
  business processes handled as free-form reasoning skip steps and aren't reproducible. Role:
  deterministic flows with validation and approval gates. Demonstrated by:
  scenario [04](../scenarios/04_refund_without_human_approval/README.md). Local reference:
  `src/dojo/integrations/chainweaver_adapter.py`, `src/dojo/flows/refund_review.py`.
- **lessonweaver — reviewed lessons.** Problem: ad hoc fixes get pasted into prompts with no
  review. Role: turn observed failures (traces) into candidate lessons, then promote a reviewed
  subset. Demonstrated by: scenario
  [07](../scenarios/07_ai_generated_auth_bypass_pr/README.md). Local reference:
  `src/dojo/integrations/lessonweaver_adapter.py`, `src/dojo/lessons/reviewed_lessons.py`.
- **VibeGuard (`vibeguard-gate`) — generated-code safety checks.** Problem: AI-generated diffs
  can weaken security while passing normal CI. Role: scan diffs and block on risky patterns.
  Demonstrated by: scenario
  [07](../scenarios/07_ai_generated_auth_bypass_pr/README.md). Local reference:
  `src/dojo/integrations/vibeguard_adapter.py`, `.github/workflows/vibeguard.yml`.
- **skdr-eval — offline routing/policy evaluation.** Problem: policy/router changes shipped on
  intuition with no replay against history. Role: evaluate a candidate change before it ships.
  Status: not represented in code yet (tracked in #39 and #49).

## How to read this page

"Stub" means a local re-implementation that demonstrates the concept and is runnable offline,
but imports nothing from the real package. As each integration lands (per the #19 children),
its row should move from **Stub** to **Integrated** and the relevant adapter docstring updated
to match.
