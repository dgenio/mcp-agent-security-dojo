"""VibeGuard adapter.

LOCAL REFERENCE IMPLEMENTATION — this is NOT the real library. The real VibeGuard
is published as ``vibeguard-gate`` (import ``vibeguard``) and ships a real diff
scanner + CI gate; this file matches three literal substrings only. See
``docs/library-map.md``.

TODO: Replace with the real ``vibeguard`` scanner over PR diffs (tracked in #25).
"""

DANGEROUS_DIFF_PATTERNS = ["or True", "auth_disabled", "bypass_authorization"]


def scan_diff(diff_text: str) -> dict:
    findings = [pattern for pattern in DANGEROUS_DIFF_PATTERNS if pattern in diff_text]
    return {
        "passed": not findings,
        "findings": findings,
        "reason": "Blocked risky auth change pattern" if findings else "No risky pattern found",
    }
