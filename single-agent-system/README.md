# Single Agent System

This project implements a Single Agent System (Cybersecurity Investigation) using LangGraph and MLflow. It serves as a foundational building block for the **AgentOps lifecycle**, providing a standardised path from local development to production deployment on Databricks Mosaic AI.

## Prerequisites

- **Databricks Workspace**: A Databricks environment (works with Standard, Premium, or the [Databricks Free Trial/Community Edition](https://www.databricks.com/try-databricks)).
  - *Note: While configured for Databricks Foundation Models, the system is modular and can be modified to use any MLflow-supported LLM provider (OpenAI, Anthropic, etc.) by updating the `ChatDatabricks` implementation.*
- **Databricks CLI**: Configured with a local profile for authentication.
- **Python 3.11+** and [`uv`](https://github.com/astral-sh/uv) for dependency management.
- **Make**: Used for automating development tasks and running the project's `Makefile` commands.

## AgentOps Lifecycle: Dev to Deployment

This repository facilitates the end-to-end lifecycle of an AI Agent on the Databricks platform:

1.  **Development (Local)**:
    - Iterate on agent logic using **LangGraph** for state management.
    - Define tools in `src/core/tools.py` and prompts in `src/core/prompts.py`.
    - Use `langgraph dev` for a local visual debugger and the [LangChain Agent Chat UI](https://docs.langchain.com/oss/python/langchain/ui) to visualise agent interactions.
2.  **Testing & Evaluation**:
    - **Unit Tests**: Validate individual tool logic.
    - **Integration Tests**: Use **LLM-as-a-judge** to evaluate agent trajectories and responses against ground truth datasets. Results are logged to the MLflow experiment, enabling review within Databricks as a first-class citizen of the platform.
3.  **Logging & Versioning**:
    - Use **MLflow** to log the agent code, configuration, and dependencies as a "Model".
    - Register the model in **Unity Catalog** for governance and version control.
4.  **Deployment**:
    - Deploy the registered model to a **Mosaic AI Agent Framework** endpoint that handles scaling and security.


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

## Agent Capabilities & Tools

The agent is designed as a **Cybersecurity Investigation Assistant**. It follows a ReAct (Reasoning and Acting) pattern to help analysts investigate potential security threats.

### Use Case: IP Investigation
The agent can take a suspicious IP address and perform a multi-step investigation to determine its risk level and origin. It uses its reasoning capabilities to decide which tool to call based on the information gathered.

### Tools
- **IP Reputation Check**: Queries a database (mocked) to retrieve safety scores, known associations with malware, and geographical information for a given IP.
- **Current Time**: Provides the agent with the current UTC time to help contextualise logs and event timestamps.

### Mocking & Data
To ensure the system is runnable out-of-the-box without requiring external API keys (like VirusTotal or AlienVault), the tools in `src/core/tools.py` currently use **mocked responses**. 
- The IP reputation tool returns predefined JSON payloads for specific test IPs.
- This allows for consistent integration testing and demonstration of the AgentOps lifecycle without external dependencies.

## Setup

1. **Install Dependencies**:

   ```bash
   make install
   ```

2. **Configuration**:

   Create a `.env` file in the root directory, refer to .env.example file.

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

To run evaluation tests:

```bash
make test-eval
```

## Deployment

To log the model to MLflow and deploy it as a Databricks Agent endpoint:

```bash
make deploy
```
