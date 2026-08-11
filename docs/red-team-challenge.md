# External red-team challenge

The most valuable contribution to this lab may be a case where the governed path fails.

Do not optimize the scenario corpus for a perfect green score. The goal is to expose where controls work, where they fail, and where they create false positives.

## Useful contributions

For a flagship scenario, contribute one of these:

- a paraphrased attack that preserves the harmful intent without matching the canonical wording;
- encoded, split, indirect, or nested untrusted instructions;
- a benign near-match that should **not** be blocked;
- a legitimate privileged request that should succeed with the right authority/approval;
- malformed or unexpected tool output;
- a timeout, unavailable control, invalid policy, or dependency failure;
- a bypass that defeats the current governed path;
- a fix accompanied by a regression case that proves the bypass used to work.

Keep everything local, synthetic, and non-destructive. Do not introduce real credentials, real PII, third-party mutations, malware, or instructions whose usefulness depends on attacking systems outside this lab.

## Required evidence for a contributed case

A useful case should state:

1. **Threat / benign behavior:** what the input is trying to demonstrate.
2. **Expected invariant:** what must or must not happen.
3. **Unsafe result:** whether the baseline exhibits the failure.
4. **DIY/reference result:** how the local mitigation behaves.
5. **Real result:** how the actual relevant library behaves when real mode is available.
6. **Residual risk:** what the result still does not prove.

For a bypass, keep the failure visible in the corpus until the underlying behavior is intentionally changed. Do not weaken the test merely to restore a green badge.

## Minimum adversarial families for flagship scenarios

Each flagship scenario should eventually cover:

- canonical attack;
- paraphrase;
- encoded/obfuscated form where applicable;
- split/indirect form where applicable;
- benign near-match;
- legitimate authorized action;
- malformed/unexpected tool output;
- control unavailable/failure path.

The exact variants should reflect the real control boundary rather than becoming a generic prompt-injection word list.

## Interpreting results

A control can be useful without being complete. Reports should distinguish:

- correctly blocked harmful behavior;
- correctly allowed legitimate behavior;
- false positives;
- false negatives / known bypasses;
- indeterminate/control-failure outcomes.

Never translate a strong result on this synthetic corpus into a production-security guarantee or certification claim.
