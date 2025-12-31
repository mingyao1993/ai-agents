.PHONY: install test test-unit test-eval run-local deploy clean help

# Variables
PYTHONPATH := $(shell pwd)/src
UV := uv run

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies using uv"
	@echo "  make test             - Run all tests"
	@echo "  make test-unit        - Run unit tests"
	@echo "  make test-eval        - Run evaluation tests"
	@echo "  make run-local              - Run the agent locally using langsmith and langgraph chat ui"
	@echo "  make deploy           - Deploy the agent to Databricks"
	@echo "  make clean            - Remove temporary files"

install:
	uv sync

test:
	$(UV) pytest

test-unit:
	$(UV) pytest tests/unit

test-eval:
	$(UV) pytest tests/evaluation

run-local:
	open https://agentchat.vercel.app/?apiUrl=http://localhost:2024&assistantId=agent
	$(UV) langgraph dev

deploy:
	uv export --no-dev --no-emit-project --output-file requirements.txt
	$(UV) python src/deploy.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .uv
