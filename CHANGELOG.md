# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

While the project is pre-1.0, minor versions may include breaking changes; these
will always be called out in the relevant entry.

## [Unreleased]

### Added

- CI/quality hardening across the GitHub Actions workflows and developer
  tooling:
  - Test matrix on Python 3.10, 3.11, and 3.12 (was 3.10 only) (#78).
  - `pytest-cov` coverage with a non-blocking term-missing report in CI;
    `make coverage` locally (#76).
  - `mypy` static type checking over `src/dojo` (lenient config); `make type`
    and a CI step (#77).
  - `bandit` security scan of the governed controls and tooling, excluding the
    intentionally-unsafe teaching modules; `make security` and
    `.github/workflows/security.yml` (#84).
  - Offline Markdown link checker (`tools/check_doc_links.py`, `make linkcheck`)
    and a CI job that fails on broken repo-relative links (#79).
  - GitHub Pages publishing for the MkDocs site via
    `.github/workflows/docs.yml` (build + link check on PRs, `gh-deploy` on
    `main`) (#97).
  - `.pre-commit-config.yaml` mirroring the ruff lint/format checks plus basic
    hygiene hooks; `make hooks` to install (#88).
  - `.github/dependabot.yml` for the `github-actions` and `pip` ecosystems (#83).
  - Aggregate `make check` target running lint, type, test, linkcheck, and
    security.

### Changed

- GitHub Actions are pinned to immutable commit SHAs (with version comments)
  instead of floating major tags (#83).
- `make lint` now also runs `ruff format --check`; the repo was formatted once
  with `ruff format` to match (#88).
- `governed_agent.py`: precise type annotations so `mypy` passes with no
  behavior change (#77).

## [0.2.0] - 2026-06-16

### Added

- Realistic unsafe baseline: `src/dojo/agents/unsafe_agent.py` is now a real
  catalog → select → execute → raw-context loop driven by a local deterministic
  "model" (`select_tool`), replacing the per-scenario hard-coded dispatch
  (#29, #6).
- Unsafe baseline realism, round two (#35, #36, #37, #38, #40):
  - `src/dojo/lessons/unreviewed_lessons.py` — an unreviewed "always trust the
    ticket notes" lesson pasted straight into the effective system prompt with no
    review step. It is what makes the agent act on instructions in untrusted
    notes; toggle it with `run_unsafe_scenario(..., apply_unreviewed_lesson=...)`.
    The lesson fixes one case (a refund denied in error) while opening a
    prompt-injection vector — the failure that motivates a reviewed lesson
    lifecycle (#37).
  - Scenario 04's refund is now **free-form reasoning over the untrusted
    ticket-400 note** — `select_tool` parses the amount/invoice from the note and
    issues the refund with no ownership/evidence check, instead of a hard-coded
    `issue_refund` call (#36).
  - `src/dojo/audit/inadequate_log.py` — a plausible-but-useless `weak_log` the
    unsafe agent emits per step (no actor / resource / rationale / args /
    timestamp), making the gap to the governed structured trace concrete (#35).
  - `examples/generated_auth_bypass.diff` is now a **valid, applicable** patch
    that flips the policy engine's default `deny` to `allow`; applying it keeps
    `make lint` and `make test` green and is invisible to the substring diff
    scanner — demonstrating CI blindness to semantic regressions (#38).
  - The governed scenario 06 emits `context_metrics` on the bounded context, so
    the raw-vs-bounded leak is a measured before/after (≈2638→121 chars,
    7→0 sensitive fields) rather than an assertion (#40).
- `src/dojo/tools/catalog.py` — a credible enterprise tool catalog with
  `description` / `side_effecting` / `risk` / `required_scope` metadata, handed
  wholesale to the unsafe agent. Adds `crm.search_customer`,
  `crm.get_customer_profile`, `email.draft_reply` / `email.send_reply`,
  `support.search_tickets` / `support.close_ticket`, `docs.search_policy`,
  `identity.lookup_user`, `admin.update_user_role`, the poisoned
  `invoice.summarize`, and `vcs.merge_pull_request` (#30).
- `src/dojo/audit/side_effects.py` — a visible side-effect ledger that records
  every side-effecting tool call (action / target / args / timestamp) with no
  approval gate; persists to `DOJO_LEDGER_DIR` when set (#34).
- `src/dojo/context/metrics.py` — context size / sensitive-field metrics for the
  raw-context-overload before/after comparison (#40).
- Scenario `08_privilege_escalation_ambient_authority` — an injected ticket note
  steers the unsafe agent into a privileged `admin.update_user_role` call; the
  governed path denies it (#33).
- Richer `examples/` fixtures: a PII-laden customer profile with an internal
  fraud note, PII ticket history, a multi-line invoice, a realistic fake secret,
  a subtly-injected `internal_refund_policy.md`, and `generated_auth_bypass.diff`
  (#31).
- Project metadata: `keywords`, `classifiers`, `license`, `authors`, and
  `project.urls` in `pyproject.toml`, plus a `docs` optional-dependency group.
- Repository trust signals: `SECURITY.md` and `CITATION.cff`.
- Contributor onboarding: `CONTRIBUTING.md` with setup, lint/test commands, an
  "add a new scenario" guide, and commit/release conventions.
- Documentation site scaffolding: `mkdocs.yml`, `docs/site-plan.md`, and a
  `make docs` / `make docs-serve` target (MkDocs + Material).
- `docs/distribution-checklist.md` — an ethical external-distribution checklist.
- Expanded `docs/consultant-playbook.md` with business-value and
  client-conversation framing.
- README badges and a documented set of recommended GitHub topics.
- `docs/assets/banner.svg` repo banner asset.

### Changed

- Scenario 01's unsafe exfiltration target is now **extracted from**
  `examples/malicious_tool_result.txt` instead of hard-coded; the `docs.*` tools
  read their content from `examples/` (#6).
- Scenario 02's poisoned tool card no longer self-incriminates with a
  `hidden_behavior` field — the poisoning now lives in the tool implementation
  (`invoice.summarize` returns payment data its description never mentions), and
  the governed path gates on the tool's verified real effect (#32).
- `policies/default_policy.yaml` denies `admin.update_user_role` on `privileged`
  resources (supports scenario 08).

## [0.1.0] - 2026-06-06

### Added

- Initial public version of the dojo: paired unsafe vs governed implementations
  across seven scenarios (prompt injection, tool-description poisoning,
  unapproved email send, refund without approval, malicious file read, raw
  tool-output context leak, AI-generated auth-bypass PR).
- Security control modules: policy engine (`allow` / `deny` / `ask`), context
  controls (ChoiceCards, context firewall, redaction), deterministic flows, and
  an audit-trace model with a safe-path writer.
- Local reference adapters under `src/dojo/integrations/` for the Weaver Stack
  libraries (AgentFence, agent-kernel, contextweaver, ChainWeaver, lessonweaver,
  VibeGuard).
- Documentation set: architecture, threat model, security model, library map,
  glossary, FAQ, recommended path, and an LLM-readable index (`llms.txt`).
- CI workflows for tests/lint and a VibeGuard scenario demo.

[Unreleased]: https://github.com/dgenio/mcp-agent-security-dojo/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/dgenio/mcp-agent-security-dojo/releases/tag/v0.2.0
[0.1.0]: https://github.com/dgenio/mcp-agent-security-dojo/releases/tag/v0.1.0
