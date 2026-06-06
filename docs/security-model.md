# Security model

The governed path is built as **defense in depth**: several independent control layers, each
with a stated guarantee and explicit limitations, arranged so that a single bypass does not
defeat the system. This document describes each layer, what it does and does not cover, and
how the layers compose. It is the companion to the [threat model](threat-model.md) (which
defines *what* we defend) and the [architecture](architecture.md) (which defines *where* each
control lives).

## Control layers

### 1. Policy engine (allow / deny / ask, default-deny)

- **What it is:** [`src/dojo/policies/engine.py`](../src/dojo/policies/engine.py).
  `PolicyEngine.decide(action, resource)` matches rules from a policy YAML and returns a
  `PolicyDecision(effect, reason)`. The governed agent reaches it through
  `AgentFenceAdapter.enforce(...)`.
- **Guarantee:** every governed action is checked against declared rules, and **no rule match
  falls through to `deny`** ("default deny"). The reported scenario status is derived from the
  effect (`allow`→allowed, `deny`→blocked, `ask`→approval_required), never hard-coded.
- **Limitations:** matching is first-rule-wins with only exact-or-`*` comparison — there is no
  specificity ranking and no glob matching, so rule order matters. Hardening this is tracked in
  #12. Conditions/thresholds (e.g. refund amount) are not yet expressible in policy (#54).

### 2. Capability tokens (scoped execution)

- **What it is:** `CapabilityToken` in
  [`src/dojo/integrations/agent_kernel_adapter.py`](../src/dojo/integrations/agent_kernel_adapter.py).
  `can_read_path(path)` resolves symlinks and `..`, and requires an exact match or a true
  directory-boundary prefix — so `/allowed_evil` cannot slip past an `/allowed` grant.
- **Guarantee:** a file read outside the granted paths is denied **before** the tool runs, even
  if policy would otherwise allow it. This is the layer scenario 05 relies on.
- **Limitations:** scoping currently covers file paths only; side-effecting actions like
  `email.send` and `refund.issue` are not capability-gated yet (tracked in #8, #52), and tokens
  have no expiry.

### 3. Context firewall (sanitization, redaction, bounded summaries)

- **What it is:** [`src/dojo/context/context_firewall.py`](../src/dojo/context/context_firewall.py):
  `sanitize_untrusted_text` neutralizes known injection patterns, `redact_sensitive_fields`
  masks email-shaped tokens, and `bounded_summary` keeps only an allow-list of fields.
- **Guarantee:** untrusted tool output is transformed before it can influence a decision
  (scenario 01), and raw records are reduced to a minimal field set before entering context
  (scenario 06).
- **Limitations:** the injection patterns and the email regex are best-effort and will miss
  novel phrasings; the field allow-list is static. This layer reduces, but does not eliminate,
  injection and leakage risk — which is why it composes with the policy layer.

### 4. Deterministic flows (known business processes)

- **What it is:** [`src/dojo/flows/refund_review.py`](../src/dojo/flows/refund_review.py):
  `run_refund_review` gathers invoice + ticket evidence, computes an `evidence_score`, and sets
  `requires_human_approval` deterministically.
- **Guarantee:** a known process follows the same validated steps every time, instead of
  free-form reasoning, and surfaces an explicit approval gate.
- **Limitations:** there is no declared I/O schema yet, so malformed input is not rejected
  fail-closed (tracked in #10/#23); only the refund process is modeled (more flows in #50).

### 5. Audit trace (auditability)

- **What it is:** [`src/dojo/audit/trace.py`](../src/dojo/audit/trace.py) +
  [`writer.py`](../src/dojo/audit/writer.py). Every governed run records `decisions`
  (action/resource/effect/reason) and `actions`, written to a uniquely named JSON file under
  `traces/` (or `DOJO_TRACE_DIR`).
- **Guarantee:** an `allow` is as auditable as a `deny` — each run leaves a durable record of
  what was decided and why. Filenames carry microsecond + random suffixes so concurrent runs
  never overwrite evidence.
- **Limitations:** the schema is intentionally thin (no request id, timestamps inside the
  payload, capabilities exercised, approval verdict, or redactions applied). A richer schema is
  tracked in #45.

### 6. CI diff safety check

- **What it is:** `scan_diff` in
  [`src/dojo/integrations/vibeguard_adapter.py`](../src/dojo/integrations/vibeguard_adapter.py),
  exercised by scenario 07.
- **Guarantee:** a diff containing a known risky pattern is flagged and the governed result is
  `blocked`.
- **Limitations:** it matches three literal substrings (`or True`, `auth_disabled`,
  `bypass_authorization`) and the CI workflow runs the scenario script rather than scanning the
  real PR diff. Making the gate scan actual diffs and use a real scanner is tracked in #11/#25.

## How the layers compose (worked example)

Scenario 01 applies **two** layers to one request:

1. The **context firewall** rewrites the injected tool output
   (`Search result... [blocked-instruction] and [blocked-instruction]`), so the exfiltration
   instruction never reaches a decision intact.
2. The **policy engine** independently denies `exfiltrate / sensitive_data`.

Either layer alone would stop this attack; together they mean a miss in the regex detector is
still caught by the policy deny, and a policy misconfiguration is still blunted by redaction.
This is the core defense-in-depth claim: **controls are independent and overlapping.**

## <a id="limitations"></a>Overall limitations

This is an **educational lab**, not a production security product:

- Detectors are deliberately simple (regex/substring) and **best-effort, not complete**.
- Tools are simulators and data is fake; nothing here has been hardened against a real adversary.
- Several controls currently demonstrate a single layer per scenario rather than the full
  pipeline; see the [threat model](threat-model.md#residual-risks-and-out-of-scope) for residual
  risks and the issue tracker for planned hardening.

Treat the guarantees above as *illustrations of the pattern*, and the limitations as the honest
edges of what the demo proves.
