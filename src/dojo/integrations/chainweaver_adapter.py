"""ChainWeaver adapter.

LOCAL REFERENCE IMPLEMENTATION — this is NOT the real library. The real
``chainweaver`` (``pip install chainweaver``) provides ``FlowBuilder``, the
``@tool`` decorator, and schema validation; this file just folds step callables
over a dict with no validation. See ``docs/library-map.md``.

TODO: Wire real ChainWeaver schema-validated flows (tracked in #23).
"""


def run_deterministic_flow(steps: list, initial_input: dict) -> dict:
    data = dict(initial_input)
    for step in steps:
        data = step(data)
    return data
