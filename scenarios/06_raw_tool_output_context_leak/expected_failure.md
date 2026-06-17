# Expected failure

**Unsafe run:** full CRM, billing, and support records are folded raw into context (`status:
risky`), including `name`, `email` (`pat@example.com`), `customer_id`, and internal notes. The
`context_metrics` report ~2638 chars and 7 sensitive fields.

**Governed run:** the bounded summary keeps only the allow-listed fields, yielding
`[{'status': 'gold'}, {'invoice_id': 'inv-100', 'status': 'paid'}, {'ticket_id': 'ticket-100', 'sentiment': 'frustrated'}]`
— no `customer_id`, no email, no notes. The same `context_metrics` hook reports ~121 chars and 0
sensitive fields (a measured before/after). The status is `redacted` and an audit trace is written.
