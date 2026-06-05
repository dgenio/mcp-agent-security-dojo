"""ChainWeaver adapter.

TODO: Wire deterministic schema-validated orchestration to real ChainWeaver APIs.
"""


def run_deterministic_flow(steps: list, initial_input: dict) -> dict:
    data = dict(initial_input)
    for step in steps:
        data = step(data)
    return data
