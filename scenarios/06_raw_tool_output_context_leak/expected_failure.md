# Expected failure

**Unsafe run:** full CRM, billing, and support records are returned raw (`status: risky`),
including `name`, `email` (`pat@example.com`), `customer_id`, and internal notes.

**Governed run:** the bounded summary keeps only the allow-listed fields, yielding
`[{'status': 'gold'}, {'invoice_id': 'inv-100', 'status': 'paid'}, {'ticket_id': 'ticket-100', 'sentiment': 'frustrated'}]`
— no `customer_id`, no email, no notes. The status is `redacted` and an audit trace is written.
