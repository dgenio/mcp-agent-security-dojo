# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

While the project is pre-1.0, minor versions may include breaking changes; these
will always be called out in the relevant entry.

## [Unreleased]

### Added

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

[Unreleased]: https://github.com/dgenio/mcp-agent-security-dojo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/dgenio/mcp-agent-security-dojo/releases/tag/v0.1.0
