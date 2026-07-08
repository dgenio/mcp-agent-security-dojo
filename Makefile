PYTHON ?= python
SCENARIO ?= 01_prompt_injection_in_tool_result

# Intentionally-vulnerable teaching modules under src/dojo, excluded from the
# security scan so it stays signal-rich (see SECURITY.md / #84).
BANDIT_EXCLUDE = src/dojo/agents/unsafe_agent.py,src/dojo/audit/inadequate_log.py,src/dojo/lessons/unreviewed_lessons.py

.DEFAULT_GOAL := help

.PHONY: help doctor setup test coverage lint type security linkcheck check hooks \
	run-unsafe run-safe demo new-scenario docs-deps docs docs-serve

help:  ## Show this help (the default target)
	@echo "mcp-agent-security-dojo — make targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

doctor:  ## Check the local environment (Python version, install, tools)
	@$(PYTHON) -c "import sys, importlib.util as u; v=sys.version_info; req=[('Python >= 3.10', v >= (3, 10)), ('dojo importable (make setup)', u.find_spec('dojo') is not None)]; opt=('ruff', 'pytest', 'mypy'); [print(('OK   ' if ok else 'FAIL ') + name) for name, ok in req]; [print(('OK   ' if u.find_spec(m) else 'WARN ') + m + (' available' if u.find_spec(m) else ' missing — run: make setup')) for m in opt]; sys.exit(0 if all(ok for _, ok in req) else 1)"

setup:  ## Editable install with dev extras (pytest, ruff, mypy, bandit, pre-commit)
	$(PYTHON) -m pip install -e .[dev]

test:  ## Run the test suite
	$(PYTHON) -m pytest -q

coverage:  ## Run tests with a term-missing coverage report
	$(PYTHON) -m pytest -q --cov --cov-report=term-missing

lint:  ## ruff check + ruff format --check
	$(PYTHON) -m ruff check src tests scenarios
	$(PYTHON) -m ruff format --check .

type:  ## Static type check (mypy over src/dojo)
	$(PYTHON) -m mypy

security:  ## bandit scan of the governed controls + tooling
	$(PYTHON) -m bandit -c pyproject.toml -q -r src/dojo tools -x $(BANDIT_EXCLUDE)

linkcheck:  ## Verify repo-relative Markdown links resolve
	$(PYTHON) tools/check_doc_links.py

check: lint type test linkcheck security  ## Everything CI enforces, in one shot

hooks:  ## Install the pre-commit hooks
	$(PYTHON) -m pre_commit install

run-unsafe:  ## Run a scenario's unsafe path (SCENARIO=NN_slug)
	$(PYTHON) scenarios/$(SCENARIO)/unsafe_run.py

run-safe:  ## Run a scenario's governed path (SCENARIO=NN_slug)
	$(PYTHON) scenarios/$(SCENARIO)/safe_run.py

demo:  ## Run scenario 01 unsafe then safe
	@echo "=== UNSAFE (Scenario 01) ==="
	$(PYTHON) scenarios/01_prompt_injection_in_tool_result/unsafe_run.py
	@echo "=== SAFE (Scenario 01) ==="
	$(PYTHON) scenarios/01_prompt_injection_in_tool_result/safe_run.py

new-scenario:  ## Scaffold scenarios/NN_SLUG/ (usage: make new-scenario SLUG=my_slug)
	$(PYTHON) tools/new_scenario.py $(SLUG)

docs-deps:  ## Install the docs extras (MkDocs + Material)
	$(PYTHON) -m pip install -e .[docs]

docs:  ## Build the MkDocs site to ./site
	$(PYTHON) -m mkdocs build

docs-serve:  ## Serve the docs locally with live reload
	$(PYTHON) -m mkdocs serve
