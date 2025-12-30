.PHONY: install test test-unit test-integration run deploy clean help

# Variables
PYTHONPATH := $(shell pwd)/src
UV := uv run

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies using uv"
	@echo "  make test             - Run all tests"
	@echo "  make test-unit        - Run unit tests"
	@echo "  make test-integration - Run integration/evaluation tests"
	@echo "  make run              - Run the agent locally"
	@echo "  make deploy           - Deploy the agent to Databricks"
	@echo "  make clean            - Remove temporary files"

install:
	uv sync

test: test-unit test-integration

test-unit:
	export PYTHONPATH=$(PYTHONPATH) && $(UV) python -m unittest discover tests/unit

test-integration:
	export PYTHONPATH=$(PYTHONPATH) && $(UV) python tests/integration/test_agent_eval.py

run:
	export PYTHONPATH=$(PYTHONPATH) && $(UV) python src/agent.py

deploy:
	$(UV) python src/deploy.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .uv
