# Contributing

Thanks for your interest in `mcp-agent-security-dojo`. This is an educational
security lab: the goal of every change is to make agent failure modes and their
governed mitigations **clearer, reproducible, and honest**. Contributions that
add a realistic scenario, sharpen a control, or improve the docs are very
welcome.

Please also read [`SECURITY.md`](SECURITY.md) — the unsafe scenarios are
intentionally vulnerable and should not be reported as security bugs.

## Project layout

```
src/dojo/           # the library: agents, policies, context, flows, audit, integrations, tools
scenarios/NN_*/     # paired unsafe_run.py / safe_run.py demos + README + expected_failure.md
policies/           # YAML policies (default / strict / human_approval)
examples/           # fake fixtures (no real data)
docs/               # architecture, threat model, security model, guides
tests/              # pytest suite
```

See [`docs/architecture.md`](docs/architecture.md) for how a request flows
through the governed pipeline and which module owns each stage.

## Development setup

Python 3.10+ is required.

```bash
make setup        # pip install -e .[dev]
make test         # pytest -q
make lint         # ruff check src tests scenarios
```

Run a scenario both ways while developing:

```bash
make run-unsafe SCENARIO=01_prompt_injection_in_tool_result
make run-safe   SCENARIO=01_prompt_injection_in_tool_result
```

Governed runs write an audit trace under `traces/` (override with
`DOJO_TRACE_DIR`). Committed sample traces are named `traces/sample_*.json`;
everything else under `traces/` is gitignored.

## Before you open a PR

Run the same checks CI runs, and make sure they pass:

```bash
make lint    # must report "All checks passed!"
make test    # must report all tests passed
```

`ruff` is configured in `pyproject.toml` (line length 100, rule sets `E`, `F`,
`I`). There is no separate type checker. CI (`.github/workflows/tests.yml`) runs
lint + tests on Python 3.10; `.github/workflows/vibeguard.yml` runs the
scenario 07 safe path.

## Coding conventions

- Match the surrounding code: absolute imports from `dojo.*`, small focused
  functions, and the existing dataclass / plain-function style.
- Keep tools **simulated** and data **fake** — no network calls, no real
  credentials, no writes outside the working tree.
- Be honest in docs and docstrings. If something is a local reference
  implementation rather than the real library, say so (see the
  `src/dojo/integrations/*_adapter.py` docstrings for the established phrasing).

## Adding a new scenario

Scenarios are the core teaching unit. To add one:

1. **Create the directory** `scenarios/NN_short_slug/` using the next number
   `NN`. Add four files, mirroring an existing scenario such as
   `scenarios/03_unapproved_email_send/`:
   - `README.md` — what breaks, what protects it, how to run it.
   - `unsafe_run.py` — reproduces the failure using the `unsafe_agent` /
     simulated tools.
   - `safe_run.py` — applies the relevant control(s) and writes an audit trace.
   - `expected_failure.md` — the unsafe failure and the safe mitigation.
2. **Reuse existing controls** from `src/dojo/` (policy engine, context
   firewall, capability tokens, deterministic flows) rather than inlining new
   logic. If a genuinely new control is needed, add it under the matching
   subpackage and document it in [`docs/security-model.md`](docs/security-model.md).
3. **Add fixtures** under `examples/` if needed — fake data only.
4. **Wire it into the docs:** add a row to the README scenario table (with
   `walkthrough` and, if you commit one, `trace` links) and to the threat-model
   per-scenario table.
5. **Add a test** in `tests/test_scenarios.py` following the existing pattern:
   assert the unsafe path exhibits the failure and the safe path blocks /
   redacts / requires approval. Keep assertions specific.

## Commit and PR conventions

- Use [Conventional Commits](https://www.conventionalcommits.org/) prefixes:
  `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`. Keep each commit
  focused.
- Reference the issue it addresses (e.g. `Closes #NN`) in the PR description.
- Keep PRs reviewable: prefer the smallest correct change, and update
  [`CHANGELOG.md`](CHANGELOG.md) under `## [Unreleased]` for any user-facing
  change.

## Release process

Releases follow [Semantic Versioning](https://semver.org/) and
[Keep a Changelog](https://keepachangelog.com/):

1. Move the `## [Unreleased]` entries in `CHANGELOG.md` into a new
   `## [X.Y.Z] - YYYY-MM-DD` section and update the comparison links at the
   bottom.
2. Bump `version` in `pyproject.toml` (and `version` in `CITATION.cff`).
3. Tag the release: `git tag vX.Y.Z && git push origin vX.Y.Z`.
4. Publish a GitHub Release from that tag, pasting the changelog section as the
   notes.

## Code of conduct

Be respectful and constructive. This project exists to help people reason about
agent security; assume good faith and keep discussion focused on the work.
