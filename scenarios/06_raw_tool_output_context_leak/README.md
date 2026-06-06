# Scenario 06 — Raw tool output context leak

## The attack

The agent collects records from several tools and dumps them, raw and unredacted, into context.
Sensitive fields (customer name, email, internal notes, full invoice) ride along even though the
task does not need them — a data-minimization failure and an injection surface.

**Real-world example:** an agent answering a billing question pulls the full CRM profile, the full
invoice, and the entire ticket history into the prompt, leaking PII and internal notes.

## Unsafe path

`unsafe_run.py` returns the full CRM + billing + support records:

```text
{'status': 'risky',
 'raw_context': {'crm': {'customer_id': 'cust-100', 'name': 'Pat Example', 'email': 'pat@example.com', ...},
                 'billing': {...}, 'support': {...}}}
```

## Governed path

The **context firewall** (`firewall_records` → `bounded_summary`) keeps only an allow-list of
fields (`ticket_id`, `invoice_id`, `status`, `sentiment`), dropping identifiers and PII:

```text
{'status': 'redacted',
 'bounded_context': [{'status': 'gold'},
                     {'invoice_id': 'inv-100', 'status': 'paid'},
                     {'ticket_id': 'ticket-100', 'sentiment': 'frustrated'}],
 'trace_path': 'traces/06_..._....json'}
```

No `customer_id`, no email, no internal notes survive into context.

## Control / library mapping

| Control | Module | Reference library |
|---|---|---|
| Bounded summary (field allow-list) | `src/dojo/context/context_firewall.py` (`bounded_summary`) | contextweaver |

## Run it

```bash
make run-unsafe SCENARIO=06_raw_tool_output_context_leak
make run-safe   SCENARIO=06_raw_tool_output_context_leak
```

## See also

- [Threat model](../../docs/threat-model.md) — boundary: *untrusted tool output*.
- [Glossary: context firewall](../../docs/glossary.md).
