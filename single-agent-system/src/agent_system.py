import mlflow
from core.agent_factory import create_agent_system
from mlflow_utils.responses_agent import LangGraphResponsesAgent

# Initialize the agent using the factory
agent_system = create_agent_system()

# Wrap the agent system with LangGraphResponsesAgent for MLflow compatibility
mlflow_agent_system = LangGraphResponsesAgent(agent_system)

# Set the model for MLflow
mlflow.models.set_model(mlflow_agent_system)
