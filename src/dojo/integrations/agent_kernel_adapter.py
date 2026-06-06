"""agent-kernel adapter.

LOCAL REFERENCE IMPLEMENTATION — this is NOT the real library. agent-kernel is
published as ``weaver-kernel`` (import ``weaver_kernel``) and provides the real
``CapabilityToken``/``Firewall``/``TraceStore`` primitives this file hand-rolls.
See ``docs/library-map.md``.

TODO: Replace with real ``weaver_kernel`` capabilities (tracked in #21).
"""

import os


class CapabilityToken:
    def __init__(self, allowed_paths: list[str] | None = None) -> None:
        self.allowed_paths = allowed_paths or []

    def can_read_path(self, path: str) -> bool:
        # Resolve symlinks and normalize ``..``/redundant separators so the
        # containment check cannot be bypassed with path tricks. A naive
        # ``startswith`` would also let ``/allowed_evil`` slip past ``/allowed``,
        # so require an exact match or a real directory-boundary prefix.
        try:
            target = os.path.realpath(path)
        except (OSError, ValueError):
            return False
        for prefix in self.allowed_paths:
            try:
                base = os.path.realpath(prefix)
            except (OSError, ValueError):
                continue
            if target == base or target.startswith(base + os.sep):
                return True
        return False
