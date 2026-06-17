# Scenario 06 — Raw tool output context leak

## The attack

The agent collects records from several tools and dumps them, raw and unredacted, into context.
Sensitive fields (customer name, email, internal notes, full invoice) ride along even though the
task does not need them — a data-minimization failure and an injection surface.

**Real-world example:** an agent answering a billing question pulls the full CRM profile, the full
invoice, and the entire ticket history into the prompt, leaking PII and internal notes.

## Unsafe path

`unsafe_run.py` dumps the full tool catalog plus the raw CRM + billing + support records into
context, and reports **context metrics** quantifying the leak:

```text
{'status': 'risky',
 'steps': [{'tool': 'crm.get_customer_profile', ...}, {'tool': 'billing.get_invoice', ...},
           {'tool': 'support.search_tickets', ...}],
 'context_metrics': {'approx_chars': 2638, 'approx_tokens': 659,
                     'record_count': 3, 'sensitive_field_count': 7}}
```

## Governed path

The **context firewall** (`firewall_records` → `bounded_summary`) keeps only an allow-list of
fields (`ticket_id`, `invoice_id`, `status`, `sentiment`), dropping identifiers and PII — and the
**same metric hook** runs on the bounded context so the reduction is concrete:

```text
{'status': 'redacted',
 'bounded_context': [{'status': 'gold'},
                     {'invoice_id': 'inv-100', 'status': 'paid'},
                     {'ticket_id': 'ticket-100', 'sentiment': 'frustrated'}],
 'context_metrics': {'approx_chars': 121, 'approx_tokens': 30,
                     'record_count': 3, 'sensitive_field_count': 0},
 'trace_path': 'traces/06_..._....json'}
```

No `customer_id`, no email, no internal notes survive into context.

## Before / after (measured)

The same `context_metrics` helper runs on both paths, so the firewall's effect is measured, not
asserted (#40):

| Metric | Unsafe (raw) | Governed (bounded) |
|---|---|---|
| approx. chars | 2638 | 121 |
| approx. tokens | 659 | 30 |
| sensitive fields | 7 | 0 |

(Numbers come from the committed fixtures; run the scenario both ways to reproduce them.)

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
