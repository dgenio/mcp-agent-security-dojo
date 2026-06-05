from pathlib import Path

from dojo.agents.governed_agent import run_governed_scenario


def test_safe_scenario_writes_trace(monkeypatch, tmp_path):
    monkeypatch.setenv("DOJO_TRACE_DIR", str(tmp_path))
    result = run_governed_scenario("01_prompt_injection_in_tool_result", repo_root=".")
    path = Path(result["trace_path"])
    assert path.exists()
    assert path.parent == tmp_path
