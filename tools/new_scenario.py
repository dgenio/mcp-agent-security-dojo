#!/usr/bin/env python3
"""Scaffold a new scenario folder from the established template.

Adding a scenario is the core contribution path (see CONTRIBUTING.md). Every
``scenarios/NN_*/`` folder has the same four files — ``README.md``,
``expected_failure.md``, ``unsafe_run.py`` and ``safe_run.py`` — with
near-identical runners. This generator computes the next ``NN``, creates the
folder, and writes those four files pre-populated from a template, so a
contributor cannot fumble the numbering or forget a file.

It deliberately does **not** edit the agents, the test matrix, or the docs:
that logic is scenario-specific and must be written by hand. Instead the
generator prints the exact remaining wiring steps when it finishes.

Run via ``make new-scenario SLUG=my_slug`` or directly:

    python tools/new_scenario.py my_slug
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
_DIR_RE = re.compile(r"^(\d{2})_")


def next_number(scenarios_dir: Path) -> str:
    """Return the next zero-padded ``NN`` scenario number as a string."""
    highest = 0
    for child in scenarios_dir.iterdir() if scenarios_dir.exists() else []:
        if not child.is_dir():
            continue
        match = _DIR_RE.match(child.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{highest + 1:02d}"


def _readme(scenario_id: str, slug: str) -> str:
    title = slug.replace("_", " ").capitalize()
    return f"""# Scenario {scenario_id[:2]} — {title}

## The attack

<!-- TODO: describe the failure the unsafe path reproduces, in plain language. -->

**Real-world example:** <!-- TODO -->

## Unsafe path

`unsafe_run.py` <!-- TODO: what side effect / leak / unapproved action happens. -->

## Governed path

`safe_run.py` <!-- TODO: which control(s) stop it and what the governed status is. -->

## Control / library mapping

| Control | Module | Reference library |
|---|---|---|
| <!-- TODO --> | `src/dojo/...` | <!-- TODO --> |

## Run it

```bash
make run-unsafe SCENARIO={scenario_id}
make run-safe   SCENARIO={scenario_id}
```

## See also

- [Threat model](../../docs/threat-model.md)
- [Security model](../../docs/security-model.md)
"""


def _expected_failure(scenario_id: str) -> str:
    return """# Expected failure

**Unsafe run:** <!-- TODO: the concrete risky outcome (status: risky). -->

**Governed run:** <!-- TODO: the control's decision and the derived status
(blocked / approval_required / redacted / allowed), plus the audit trace. -->
"""


def _unsafe_run(scenario_id: str) -> str:
    return f"""from dojo.agents.unsafe_agent import run_unsafe_scenario

if __name__ == "__main__":
    print(run_unsafe_scenario("{scenario_id}", repo_root="."))
"""


def _safe_run(scenario_id: str) -> str:
    return f"""from dojo.agents.governed_agent import run_governed_scenario

if __name__ == "__main__":
    print(run_governed_scenario("{scenario_id}", repo_root="."))
"""


def scaffold(slug: str, scenarios_dir: Path) -> Path:
    """Create ``scenarios/NN_slug/`` with the four standard files.

    Returns the created folder path. Raises ``ValueError`` for a bad slug and
    ``FileExistsError`` if a folder for the slug already exists.
    """
    if not _SLUG_RE.match(slug):
        raise ValueError(
            f"invalid slug {slug!r}: use lowercase snake_case, e.g. 'malicious_file_read'"
        )
    number = next_number(scenarios_dir)
    scenario_id = f"{number}_{slug}"
    folder = scenarios_dir / scenario_id
    if folder.exists():
        raise FileExistsError(f"{folder} already exists")
    for existing in scenarios_dir.iterdir() if scenarios_dir.exists() else []:
        if not existing.is_dir():
            continue
        # Compare the slug portion after the ``NN_`` prefix, not a suffix match:
        # an existing ``01_new_thing`` must not block a new slug ``thing``.
        match = _DIR_RE.match(existing.name)
        existing_slug = existing.name[match.end() :] if match else existing.name
        if existing_slug == slug:
            raise FileExistsError(f"a scenario for slug {slug!r} already exists: {existing.name}")

    folder.mkdir(parents=True)
    (folder / "README.md").write_text(_readme(scenario_id, slug), encoding="utf-8")
    (folder / "expected_failure.md").write_text(_expected_failure(scenario_id), encoding="utf-8")
    (folder / "unsafe_run.py").write_text(_unsafe_run(scenario_id), encoding="utf-8")
    (folder / "safe_run.py").write_text(_safe_run(scenario_id), encoding="utf-8")
    return folder


def _remaining_steps(scenario_id: str) -> str:
    return f"""
Created scenarios/{scenario_id}/ with README.md, expected_failure.md,
unsafe_run.py and safe_run.py.

Remaining wiring (scenario-specific — do by hand):
  1. Add a per-scenario branch/config in src/dojo/agents/unsafe_agent.py
     (_build_tasks) and src/dojo/agents/governed_agent.py.
  2. Add "{scenario_id}" to SCENARIOS and EXPECTED_GOVERNED_STATUS in
     tests/test_scenarios.py.
  3. Add a row to the README scenario map and the docs/threat-model.md table.
  4. Add a CHANGELOG.md [Unreleased] entry.

See the "Adding a new scenario" guide in CONTRIBUTING.md.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new dojo scenario.")
    parser.add_argument("slug", help="lowercase snake_case slug, e.g. malicious_file_read")
    default_dir = Path(__file__).resolve().parent.parent / "scenarios"
    parser.add_argument(
        "--scenarios-dir",
        type=Path,
        default=default_dir,
        help="scenarios directory (default: the repo's scenarios/)",
    )
    args = parser.parse_args(argv)
    try:
        folder = scaffold(args.slug, args.scenarios_dir)
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(_remaining_steps(folder.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
