import pytest

from dojo.agents.governed_agent import run_governed_scenario
from dojo.agents.unsafe_agent import run_unsafe_scenario

SCENARIOS = [
    "01_prompt_injection_in_tool_result",
    "02_tool_description_poisoning",
    "03_unapproved_email_send",
    "04_refund_without_human_approval",
    "05_malicious_file_read",
    "06_raw_tool_output_context_leak",
    "07_ai_generated_auth_bypass_pr",
]


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_unsafe_scenarios_show_risky_behavior(scenario):
    result = run_unsafe_scenario(scenario, repo_root=".")
    assert result["status"] == "risky"


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_governed_scenarios_apply_controls(monkeypatch, tmp_path, scenario):
    monkeypatch.setenv("DOJO_TRACE_DIR", str(tmp_path))
    result = run_governed_scenario(scenario, repo_root=".")
    assert result["status"] in {"blocked", "approval_required", "redacted", "allowed"}
    assert "trace_path" in result
