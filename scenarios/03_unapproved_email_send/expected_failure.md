# Expected failure

**Unsafe run:** an email is actually *sent* to `customer@example.com` with no approval
(`status: risky`; `email.send_reply` in the side-effect ledger). The team's `weak_log` records
only `"INFO: handled request"` — no actor, resource, rationale, args, or timestamp (#35).

**Governed run:** the policy engine returns `effect=ask` (reason: *"Human approval required
before sending customer email."*), the email is produced as a **draft** (`mode: draft`) instead
of being sent, the status is `approval_required`, and an audit trace is written.
