PYTHON ?= python
SCENARIO ?= 01_prompt_injection_in_tool_result

# Intentionally-vulnerable teaching modules under src/dojo, excluded from the
# security scan so it stays signal-rich (see SECURITY.md / #84).
BANDIT_EXCLUDE = src/dojo/agents/unsafe_agent.py,src/dojo/audit/inadequate_log.py,src/dojo/lessons/unreviewed_lessons.py

.PHONY: setup test coverage lint type security linkcheck check hooks \
	run-unsafe run-safe demo docs-deps docs docs-serve

setup:
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m pytest -q

coverage:
	$(PYTHON) -m pytest -q --cov --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check src tests scenarios
	$(PYTHON) -m ruff format --check .

type:
	$(PYTHON) -m mypy

security:
	$(PYTHON) -m bandit -c pyproject.toml -q -r src/dojo tools -x $(BANDIT_EXCLUDE)

linkcheck:
	$(PYTHON) tools/check_doc_links.py

# Everything CI enforces, in one shot.
check: lint type test linkcheck security

hooks:
	$(PYTHON) -m pre_commit install

run-unsafe:
	$(PYTHON) scenarios/$(SCENARIO)/unsafe_run.py

run-safe:
	$(PYTHON) scenarios/$(SCENARIO)/safe_run.py

demo:
	@echo "=== UNSAFE (Scenario 01) ==="
	$(PYTHON) scenarios/01_prompt_injection_in_tool_result/unsafe_run.py
	@echo "=== SAFE (Scenario 01) ==="
	$(PYTHON) scenarios/01_prompt_injection_in_tool_result/safe_run.py

docs-deps:
	$(PYTHON) -m pip install -e .[docs]

docs:
	$(PYTHON) -m mkdocs build

docs-serve:
	$(PYTHON) -m mkdocs serve
