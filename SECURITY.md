# Security policy

`mcp-agent-security-dojo` is an **educational security lab and reference
architecture**. It deliberately reproduces insecure agent behaviours so they can
be studied and then governed. This document explains what that means for the
project's own security posture and how to report a problem.

## Important context

- **The unsafe scenarios are intentionally vulnerable.** Code under
  `scenarios/*/unsafe_run.py` and the `unsafe_agent` path exist to *demonstrate*
  failure modes (prompt injection, tool poisoning, over-permissioned tools,
  unapproved side effects, context leakage, auth-weakening diffs). These are not
  bugs — they are the teaching material. Please do not report them as
  vulnerabilities.
- **No real secrets, credentials, or network calls.** Every tool is a local
  simulator and every fixture under `examples/` is fake data. Files such as
  `examples/internal_secrets.txt` contain invented values used only to show how
  the governed path blocks or redacts them.
- **Not production-ready.** The detectors are deliberately simple (regex /
  substring) and the controls illustrate patterns rather than provide hardened
  enforcement. See [`docs/security-model.md`](docs/security-model.md#limitations)
  for the explicit limitations.

## What *is* in scope for a report

Report anything that undermines the lab's stated guarantees or could harm a user
who runs it as documented, for example:

- A scenario or test that performs a **real** side effect — a network call, a
  write outside the repo working tree, or execution of untrusted input on the
  host.
- A flaw in a control that is described as *enforcing* something in the
  **governed** path (e.g. the capability path check or context firewall) that
  lets the governed path leak or act when the docs say it should not.
- Exposure of a real secret accidentally committed to the repository.
- A vulnerability in the project's tooling, CI workflows, or build configuration.

## Automated scanning scope

A [`bandit`](https://bandit.readthedocs.io/) static-analysis job
(`.github/workflows/security.yml`, run locally via `make security`) scans the
**governed controls and the project's own tooling** — `src/dojo/` and `tools/` —
which is the surface this policy puts in scope. The intentionally-vulnerable
teaching modules are deliberately **excluded** so the scan stays signal-rich
instead of flagging the lab's designed-in failure modes:

- `src/dojo/agents/unsafe_agent.py`
- `src/dojo/audit/inadequate_log.py`
- `src/dojo/lessons/unreviewed_lessons.py`
- everything under `scenarios/` (each `unsafe_run.py` is teaching material)

The exclusion list lives in the `Makefile` (`BANDIT_EXCLUDE`) and
`[tool.bandit]` in `pyproject.toml`. If you add a new intentionally-unsafe
module, extend the exclusion and note why in its docstring; do **not** "fix" a
deliberate weakness to satisfy the scanner.

## Reporting a vulnerability

Please report privately rather than opening a public issue:

1. Preferred: use GitHub's **“Report a vulnerability”** flow under the
   repository's **Security** tab (Security advisories).
2. Alternatively, open a minimal private report and avoid posting working
   exploit details publicly until a fix is available.

Please include:

- The affected file(s), scenario, or workflow.
- Steps to reproduce and what you observed versus what the documentation claims.
- Why you believe it is in scope per the section above.

## Response expectations

This is a volunteer-maintained educational project, so there is no formal SLA.
Reports that fall in scope will be acknowledged and triaged on a best-effort
basis, and credited in the [changelog](CHANGELOG.md) unless you prefer otherwise.

## Supported versions

Only the latest `main` is maintained. There is no backport policy.
