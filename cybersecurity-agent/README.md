# Cybersecurity Investigation Agent

This project implements a production-ready Cybersecurity Investigation Agent using LangGraph and MLflow, designed for deployment on Databricks.

## Project Structure

- `src/`: Main source code.
  - `agent.py`: Agent definition and MLflow model entry point.
  - `deploy.py`: Deployment script to log and register the model to MLflow/Unity Catalog.
  - `core/`: Core logic and configuration.
    - `config.py`: Configuration management using Pydantic Settings.
    - `agent_factory.py`: Factory for creating agent instances.
    - `tools.py`: Tool definitions (e.g., IP reputation check, time).
    - `prompts.py`: System prompts for the agent.
  - `mlflow_helpers/`: Utilities for MLflow integration.
  - `utils/`: General utility functions.
- `tests/`:
  - `unit/`: Unit tests for individual components (e.g., tools).
  - `integration/`: Integration and evaluation tests using LLM judges.
- `scripts/`: Helper scripts for deployment and experimentation.

## Setup

1. **Install Dependencies**:

   ```bash
   make install
   ```

2. **Configuration**:

   Create a `.env` file in the root directory and set the following variables:

   ```env
   LLM_ENDPOINT_NAME=your-databricks-endpoint
   MLFLOW_TRACKING_URI=databricks
   MLFLOW_EXPERIMENT_PATH=/Shared/your-experiment
   ```

## Running Locally

To test the agent locally:

```bash
make run
```

## Running Tests

To run all tests:

```bash
make test
```

To run only unit tests:

```bash
make test-unit
```

To run integration/evaluation tests:

```bash
make test-integration
```

## Deployment

To log the model to MLflow and deploy it as a Databricks Agent endpoint:

```bash
make deploy
```

## Development

- **Add a new tool**: Define it in `src/core/tools.py` and add it to the `tools` list in `src/core/agent_factory.py`.
- **Update prompts**: Modify `src/core/prompts.py`.
- **Change configuration**: Update `src/core/config.py` or the `.env` file.

[Agent Chat](https://agentchat.vercel.app/)

```bash
uv run langgraph dev
source .venv/bin/activate
python -m ensurepip
uv pip compile --output-file requirements.txt pyproject.toml
```
