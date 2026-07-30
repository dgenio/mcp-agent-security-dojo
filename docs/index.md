# mcp-agent-security-dojo

A hands-on security dojo for MCP-style and tool-using AI agents: reproduce common
failure modes, then govern them with policy gates, bounded context, deterministic
flows, capability scoping, and audit traces.

!!! warning "Educational lab — not production-ready"
    The detectors are deliberately simple, the tools are simulators, and the data
    is fake. Treat this as a reference architecture, not a drop-in security
    product. See the [security model](security-model.md#limitations) for the
    explicit limitations.

## Where to start

- **New here?** Follow the [recommended path](recommended-path.md) — watch one
  attack fail unsafely, understand why, then watch the governed path stop it.
- **Want the design?** Read the [architecture](architecture.md), then the
  [threat model](threat-model.md) and [security model](security-model.md).
- **Evaluating the libraries?** See the [library map](library-map.md) for the
  Weaver Stack and its current (honest) integration status.

## The eight scenarios

Each scenario ships an unsafe baseline that reproduces a failure and a governed
path that applies controls. Run any one with:

```bash
make run-unsafe SCENARIO=01_prompt_injection_in_tool_result
make run-safe   SCENARIO=01_prompt_injection_in_tool_result
```

| # | Failure mode | Governing control |
|---|---|---|
| 01 | Prompt injection in tool result | Context firewall + policy deny |
| 02 | Tool-description poisoning | Verified ChoiceCard + policy deny |
| 03 | Unapproved email send | Policy `ask` → draft pending approval |
| 04 | Refund without human approval | Deterministic flow + threshold |
| 05 | Malicious file read | Capability token scoping |
| 06 | Raw tool-output context leak | Bounded summary / redaction |
| 07 | AI-generated auth-bypass PR | Diff safety check + reviewed lessons |
| 08 | Privilege escalation via ambient authority | Policy deny + capability scoping |

## Reference

- [Glossary](glossary.md) and [FAQ](faq.md) for terminology and common questions.
- [Consultant playbook](consultant-playbook.md) for using the dojo with clients.
- [Distribution checklist](distribution-checklist.md) before sharing externally.

This site is built from the same Markdown under [`docs/`](https://github.com/dgenio/mcp-agent-security-dojo/tree/main/docs)
that you can also read directly on GitHub. See the [site plan](site-plan.md) for
how it is built and published.
