PYTHON ?= python
SCENARIO ?= 01_prompt_injection_in_tool_result

.PHONY: setup test lint run-unsafe run-safe demo docs-deps docs docs-serve

setup:
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check src tests scenarios

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
