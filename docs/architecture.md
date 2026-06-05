# Architecture

The dojo has two paths:

- `unsafe_agent`: direct tool invocation and raw context handling.
- `governed_agent`: policy + capability checks, bounded context, deterministic flows, audit traces, and reviewed lessons.

Core modules live under `src/dojo/` and scenario runners under `scenarios/`.
