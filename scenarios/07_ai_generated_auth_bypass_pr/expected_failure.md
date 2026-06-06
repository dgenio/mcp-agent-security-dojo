# Expected failure

**Unsafe run:** the auth-weakening diff (`if user.is_admin or True:`) is treated as merged
(`status: risky`, `merged: True`).

**Governed run:** the diff scan returns `passed: False` with `findings: ['or True']` (reason:
*"Blocked risky auth change pattern"*), the status is `blocked`, the reviewed lessons are
surfaced, and an audit trace is written.

> Note: the scanner is a best-effort substring check (see scenario README) — realistic-diff and
> real-scanner upgrades are tracked in #11, #25, and #38.
