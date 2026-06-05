"""VibeGuard adapter.

TODO: Replace with real VibeGuard CI integration.
"""


DANGEROUS_DIFF_PATTERNS = ["or True", "auth_disabled", "bypass_authorization"]


def scan_diff(diff_text: str) -> dict:
    findings = [pattern for pattern in DANGEROUS_DIFF_PATTERNS if pattern in diff_text]
    return {
        "passed": not findings,
        "findings": findings,
        "reason": "Blocked risky auth change pattern" if findings else "No risky pattern found",
    }
