"""agent-kernel adapter.

TODO: Replace fallback with real capability/context firewall support from agent-kernel.
"""


class CapabilityToken:
    def __init__(self, allowed_paths: list[str] | None = None) -> None:
        self.allowed_paths = allowed_paths or []

    def can_read_path(self, path: str) -> bool:
        return any(path.startswith(prefix) for prefix in self.allowed_paths)
