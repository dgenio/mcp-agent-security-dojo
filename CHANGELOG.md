# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

While the project is pre-1.0, minor versions may include breaking changes; these
will always be called out in the relevant entry.

## [Unreleased]

### Added

## [0.2.0] - 2026-06-16

### Added

- Realistic unsafe baseline: `src/dojo/agents/unsafe_agent.py` is now a real
  catalog → select → execute → raw-context loop driven by a local deterministic
  "model" (`select_tool`), replacing the per-scenario hard-coded dispatch
  (#29, #6).
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
