# Human approval evidence

The dojo models human approval as a state transition, not a boolean pause:

`policy decision → pending approval → human verdict → optional execution outcome`

A pending request is bound to the exact reviewed action envelope: run, actor, action, target, canonical argument digest, policy version, request id, and expiry. If a security-relevant payload or binding changes, the prior approval becomes stale and cannot authorize execution.

The built-in approval manager is an educational, in-memory implementation. Its default reviewer identity (`simulated-human`) and timestamps are **simulated evidence**, not proof of an authenticated human identity. A production host should authenticate the reviewer and provide its own identity/time evidence.

The flagship email and refund scenarios exercise `policies/human_approval_policy.yaml`. With no verdict they stop at a pending request and perform no side effect; an explicit approval can proceed to the simulated side effect, while rejection remains a distinct audited outcome.
