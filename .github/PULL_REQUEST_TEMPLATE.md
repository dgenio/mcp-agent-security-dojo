<!--
Thanks for contributing! Keep PRs focused and reviewable.
See the "Definition of done" checklist in ../CONTRIBUTING.md.
-->

## What changed

<!-- Bullet list of changes, ideally file by file. -->

## Why

<!-- Rationale grounded in the issue. Reference it below. -->

Closes #

## How verified

<!-- Exact commands run + summarized results, e.g. `make check` output. -->

```text

```

## Definition of done

- [ ] `make check` passes locally (lint + type + test + linkcheck + security), or the failing steps and why are noted above.
- [ ] New/changed behaviour is tested (happy path **and** a failure/edge case), with specific assertions.
- [ ] Docs surfaces updated where relevant (README scenario map, `docs/*`, scenario READMEs).
- [ ] [`CHANGELOG.md`](../CHANGELOG.md) `## [Unreleased]` updated for any user-facing change.
- [ ] Tools stay simulated and data stays fake — no network, no real credentials, no writes outside the working tree (see [`SECURITY.md`](../SECURITY.md)).
- [ ] Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`).

## Notes / risks

<!-- Tradeoffs, follow-ups, or "None identified". -->
