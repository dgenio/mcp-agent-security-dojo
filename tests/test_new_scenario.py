"""Tests for the scenario scaffolding generator (``tools/new_scenario.py``).

``tools/`` is not an importable package, so the module is loaded by file path
(mirroring ``tests/test_check_doc_links.py``).
"""

import importlib.util
from pathlib import Path

import pytest

_MODULE_PATH = Path(__file__).resolve().parent.parent / "tools" / "new_scenario.py"
_spec = importlib.util.spec_from_file_location("new_scenario", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
new_scenario = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(new_scenario)


def _seed(scenarios_dir: Path, *names: str) -> None:
    for name in names:
        (scenarios_dir / name).mkdir(parents=True)


def test_next_number_continues_the_sequence(tmp_path):
    _seed(tmp_path, "01_alpha", "02_beta", "03_gamma")
    assert new_scenario.next_number(tmp_path) == "04"


def test_next_number_starts_at_01_when_empty(tmp_path):
    assert new_scenario.next_number(tmp_path) == "01"


def test_next_number_ignores_non_scenario_dirs(tmp_path):
    _seed(tmp_path, "01_alpha", "notes")
    (tmp_path / "README.md").write_text("x\n", encoding="utf-8")
    assert new_scenario.next_number(tmp_path) == "02"


def test_scaffold_creates_all_four_files_with_correct_id(tmp_path):
    _seed(tmp_path, "01_alpha")
    folder = new_scenario.scaffold("malicious_file_read", tmp_path)

    assert folder.name == "02_malicious_file_read"
    files = {p.name for p in folder.iterdir()}
    assert files == {"README.md", "expected_failure.md", "unsafe_run.py", "safe_run.py"}

    # Runners reference the new scenario id and the real agent entry points.
    unsafe = (folder / "unsafe_run.py").read_text(encoding="utf-8")
    safe = (folder / "safe_run.py").read_text(encoding="utf-8")
    assert 'run_unsafe_scenario("02_malicious_file_read"' in unsafe
    assert "from dojo.agents.unsafe_agent import run_unsafe_scenario" in unsafe
    assert 'run_governed_scenario("02_malicious_file_read"' in safe
    assert "from dojo.agents.governed_agent import run_governed_scenario" in safe

    # README run commands use the new scenario id.
    readme = (folder / "README.md").read_text(encoding="utf-8")
    assert "SCENARIO=02_malicious_file_read" in readme


def test_scaffold_rejects_invalid_slug(tmp_path):
    with pytest.raises(ValueError):
        new_scenario.scaffold("Bad-Slug", tmp_path)


def test_scaffold_rejects_duplicate_slug(tmp_path):
    _seed(tmp_path, "01_taken")
    with pytest.raises(FileExistsError):
        new_scenario.scaffold("taken", tmp_path)


def test_scaffold_allows_slug_that_is_a_suffix_of_an_existing_slug(tmp_path):
    # Regression: an existing "01_new_thing" must not block the distinct slug
    # "thing" (the duplicate check compares the full slug, not a suffix match).
    _seed(tmp_path, "01_new_thing")
    folder = new_scenario.scaffold("thing", tmp_path)
    assert folder.name == "02_thing"


def test_main_returns_nonzero_on_bad_slug(tmp_path, capsys):
    rc = new_scenario.main(["Bad Slug", "--scenarios-dir", str(tmp_path)])
    assert rc == 1
    assert "error" in capsys.readouterr().err


def test_main_scaffolds_and_prints_remaining_steps(tmp_path, capsys):
    rc = new_scenario.main(["new_thing", "--scenarios-dir", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / "01_new_thing").is_dir()
    assert "Remaining wiring" in capsys.readouterr().out
