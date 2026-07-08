"""Tests for the environment doctor (``tools/doctor.py``).

``tools/`` is not an importable package, so the module is loaded by file path
(mirroring ``tests/test_new_scenario.py``).
"""

import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "tools" / "doctor.py"
_spec = importlib.util.spec_from_file_location("doctor", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
doctor = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(doctor)


def test_render_marks_required_pass_and_fail():
    lines = doctor.render([("Python >= 3.10", True), ("dojo importable", False)], [])
    assert lines == ["OK   Python >= 3.10", "FAIL dojo importable"]


def test_render_marks_optional_available_and_missing():
    lines = doctor.render([], [("ruff", True), ("pytest", False)])
    assert lines == ["OK   ruff available", "WARN pytest missing — run: make setup"]


def test_passed_is_true_only_when_all_required_ok():
    assert doctor.passed([("a", True), ("b", True)]) is True
    assert doctor.passed([("a", True), ("b", False)]) is False


def test_main_exits_zero_when_environment_is_healthy(monkeypatch, capsys):
    monkeypatch.setattr(
        doctor,
        "required_checks",
        lambda: [("Python >= 3.10", True), ("dojo importable (make setup)", True)],
    )
    monkeypatch.setattr(doctor, "optional_checks", lambda: [("ruff", True)])
    assert doctor.main() == 0
    out = capsys.readouterr().out
    assert "OK   Python >= 3.10" in out
    assert "OK   ruff available" in out


def test_main_exits_nonzero_when_required_check_fails(monkeypatch, capsys):
    monkeypatch.setattr(
        doctor,
        "required_checks",
        lambda: [("dojo importable (make setup)", False)],
    )
    monkeypatch.setattr(doctor, "optional_checks", lambda: [("pytest", False)])
    assert doctor.main() == 1
    out = capsys.readouterr().out
    assert "FAIL dojo importable (make setup)" in out
    assert "WARN pytest missing — run: make setup" in out
