"""Tests for the realistic AI-generated auth-weakening diff fixture (#38).

The fixture must be a *credible* regression: it weakens a real security property
(the policy engine's deny-by-default fallback), it is a valid patch that applies
to the current source, and it is invisible to the naive substring scanner — the
whole point being that format + test gates do not catch semantic safety
regressions.
"""

from pathlib import Path

from dojo.integrations.vibeguard_adapter import DANGEROUS_DIFF_PATTERNS, scan_diff

DIFF = Path("examples/generated_auth_bypass.diff")
ENGINE = Path("src/dojo/policies/engine.py")


def _diff_text() -> str:
    return DIFF.read_text(encoding="utf-8")


def test_diff_is_realistic_not_a_strawman():
    text = _diff_text()
    # No "or True"-style tell; nothing the naive substring scanner could catch.
    assert "or True" not in text
    for pattern in DANGEROUS_DIFF_PATTERNS:
        assert pattern not in text


def test_diff_weakens_default_deny_to_default_allow():
    text = _diff_text()
    # The removed line is the deny-by-default fallback; the added line fails open.
    assert '-        return PolicyDecision(effect="deny", reason="default deny")' in text
    assert '+        return PolicyDecision(effect="allow", reason="default allow")' in text


def test_diff_targets_the_real_default_fallback_line():
    # The patch flips the engine's default fallback. Accept either the pristine
    # (deny) or applied (allow) form so the fixture can't silently rot and the
    # apply/revert demonstration stays green in both states.
    engine = ENGINE.read_text(encoding="utf-8")
    assert (
        '        return PolicyDecision(effect="deny", reason="default deny")\n' in engine
        or '        return PolicyDecision(effect="allow", reason="default allow")\n' in engine
    )


def test_naive_scanner_is_blind_to_the_realistic_diff():
    # scenario 07's substring scanner passes the diff — demonstrating CI blindness
    # (a real semantic scanner is tracked in #25).
    result = scan_diff(_diff_text())
    assert result["passed"] is True
    assert result["findings"] == []
