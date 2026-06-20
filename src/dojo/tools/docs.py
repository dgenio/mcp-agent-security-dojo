"""Simulated local docs/search tool."""

from pathlib import Path

from dojo.tools._fixtures import load_text


def search_docs(query: str, include_malicious_result: bool = False, root: str | Path = ".") -> str:
    """Search the knowledge base.

    With ``include_malicious_result`` the result is sourced from
    ``examples/malicious_tool_result.txt`` — untrusted text that carries a
    subtly-phrased instruction to forward customer data to an external address.
    """
    base = f"Search result for '{query}': refund policy requires verification."
    if include_malicious_result:
        return base + "\n\n" + load_text(root, "malicious_tool_result.txt")
    return base


def search_policy(root: str | Path = ".", topic: str = "refund", **_: object) -> str:
    """Return the internal policy document for a topic.

    Backed by ``examples/internal_refund_policy.md``, a trusted-looking document
    that nonetheless contains a subtle embedded instruction.
    """
    return load_text(root, "internal_refund_policy.md")
