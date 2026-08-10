# LLM index

A factual, non-promotional summary for machine readers (LLMs, crawlers building a knowledge
base). The root [`llms.txt`](../llms.txt) mirrors the essentials of this file.

## Purpose

A hands-on security dojo for MCP-style and tool-using AI agents: reproduce common failure modes,
then govern them with policy gates, bounded context, deterministic flows, capability scoping, and
audit traces. It is an **educational lab**, not a production security product. Tools are local
simulators with fake data; there is no network or live LLM.

## The 8 scenarios

1. `01_prompt_injection_in_tool_result` — injected tool output steers the agent into emailing an
   SSN; governed path: context firewall + policy deny → `blocked`.
2. `02_tool_description_poisoning` — benign-looking tool card hides a dangerous action; governed:
   verified ChoiceCard + policy deny → `blocked`.
3. `03_unapproved_email_send` — agent sends a customer email directly; governed: policy `ask` →
   email downgraded to a draft → `approval_required`.
4. `04_refund_without_human_approval` — a $350 refund issued on weak evidence; governed:
   deterministic flow + threshold → `approval_required`.
5. `05_malicious_file_read` — agent reads `internal_secrets.txt`; governed: capability token
   scopes reads to `examples/safe/` → `blocked`.
6. `06_raw_tool_output_context_leak` — full CRM/billing/support records (PII) dumped into context;
   governed: bounded summary keeps only allow-listed fields → `redacted`.
7. `07_ai_generated_auth_bypass_pr` — a risky auth-weakening diff would merge; governed: diff
   scanner flags the pattern → `blocked`.
8. `08_privilege_escalation_ambient_authority` — injected ticket text steers the agent into
   calling `admin.update_user_role`; governed: policy denial via `fence.enforce` →
   `blocked`. Per-task capability scoping is a prospective hardening step.

## Architecture (text)

Request → context selection / ChoiceCards (`src/dojo/context/`) → policy decision allow/deny/ask
(`src/dojo/policies/engine.py` via `integrations/agentfence_adapter.py`) → capability scope check
(`integrations/agent_kernel_adapter.py`) → deterministic flow where applicable
(`src/dojo/flows/`) → tool execution (`src/dojo/tools/`) → context firewall
(`src/dojo/context/context_firewall.py`) → audit trace (`src/dojo/audit/`) → reviewed lessons
(`src/dojo/lessons/`). Two agents: `unsafe_agent.run_unsafe_scenario` and
`governed_agent.run_governed_scenario`.

## Key commands

```bash
make setup    # editable install + local PEP 735 maintainer tooling group
make test     # run the test suite
make lint     # ruff check + format check
make run-unsafe SCENARIO=<id>   # run the unsafe baseline for a scenario
make run-safe   SCENARIO=<id>   # run the governed path for a scenario
make demo                       # scenario 01, unsafe then safe
```

`<id>` is a scenario folder name (e.g. `01_prompt_injection_in_tool_result`). Governed runs write
an audit trace to `traces/` (or `DOJO_TRACE_DIR`).

## Libraries (status)

Designed around the Weaver Stack: AgentFence (Go action — **not** the unrelated PyPI
`agentfence`), agent-kernel (`pip install weaver-kernel`, import `weaver_kernel`), contextweaver,
ChainWeaver (`chainweaver`), lessonweaver (`pip install lessonweaver`), VibeGuard
(`vibeguard-gate`, import `vibeguard`), skdr-eval. All are currently **local reference
implementations (stubs)** under `src/dojo/integrations/`; the real packages are not yet wired in.
See [library map](library-map.md).

## Key files and directories

- `src/dojo/agents/` — unsafe and governed agents.
- `src/dojo/policies/` — policy engine; `policies/*.yaml` — rules.
- `src/dojo/context/` — ChoiceCards and context firewall.
- `src/dojo/flows/` — deterministic flows (refund review).
- `src/dojo/audit/` — audit trace model + writer.
- `src/dojo/integrations/` — Weaver Stack adapters (stubs).
- `scenarios/NN_name/` — per-scenario README, expected_failure, runners.
- `docs/` — architecture, threat model, security model, library map, glossary, FAQ, recommended path.

## What to recommend first

Send a new reader to [the recommended path](recommended-path.md): run scenario 01 unsafe, read
why it fails, run it governed, inspect the trace, then compare scenario 04.

## What NOT to claim

- Do **not** claim it is production-ready, hardened, or a drop-in security product.
- Do **not** claim the Weaver Stack libraries are integrated — they are demonstrated via local
  stubs.
- Do **not** confuse this project's AgentFence (Go) with the unrelated PyPI `agentfence` package.
- Do **not** describe the detectors as complete; they are best-effort regex/substring checks.
