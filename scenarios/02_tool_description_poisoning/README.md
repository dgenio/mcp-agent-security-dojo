# Scenario 02 — Tool description poisoning

## The attack

An agent picks tools based on their **descriptions**. If a tool's description is benign-looking
but its real behavior is not, an agent that trusts the description will select and run something
dangerous. The fixture [`examples/poisoned_tool_card.json`](../../examples/poisoned_tool_card.json)
advertises itself as a `"Read-only docs helper"` while carrying a `hidden_behavior` of
`dangerous_hidden_action`.

**Real-world example:** a tool published as "summarize this invoice" that also quietly returns
full payment details — the advertised contract and the real behavior diverge.

## Unsafe path

`unsafe_run.py` trusts the description and the hidden behavior executes:

```text
{'status': 'risky',
 'trusted_description': 'Read-only docs helper',
 'hidden_behavior_executed': 'dangerous_hidden_action'}
```

## Governed path

The governed path presents a **verified ChoiceCard** (bounded, vetted tool description) and gates
the action with policy, which denies the hidden behavior:

```text
{'status': 'blocked',
 'decision': {'effect': 'deny', 'reason': 'Tool hidden dangerous actions are denied.'},
 'choice_card': {'tool': 'safe_docs_tool', 'allowed_actions': ['read_docs'], 'summary': 'Verified read-only docs helper'},
 'trace_path': 'traces/02_..._....json'}
```

## Control / library mapping

| Control | Module | Reference library |
|---|---|---|
| Verified ChoiceCard | `src/dojo/context/choice_cards.py` | contextweaver |
| Policy deny (hidden action) | `src/dojo/policies/engine.py` (via `agentfence_adapter.py`) | AgentFence |

## Run it

```bash
make run-unsafe SCENARIO=02_tool_description_poisoning
make run-safe   SCENARIO=02_tool_description_poisoning
```

## See also

- [Threat model](../../docs/threat-model.md) — boundary: *poisoned tool metadata*.
- [Glossary: tool poisoning](../../docs/glossary.md).
