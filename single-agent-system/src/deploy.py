import datetime
import mlflow
from core.config import settings
from databricks import agents

# Constants
CODE_PATH = "src/agent_system.py"
ENDPOINT_NAME = "single-agent-system-endpoint"
FULL_UC_MODEL_NAME = f"{settings.UC_CATALOG}.{settings.UC_SCHEMA}.{settings.UC_MODEL_NAME}"

def run_deployment():
  # MLflow Configuration
  mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
  mlflow.set_registry_uri(settings.MLFLOW_REGISTRY_URI)
  mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_PATH)

  timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  run_name = f"pipeline_run_{timestamp}"

  with mlflow.start_run(run_name=run_name):
    print(f"Logging model to MLflow: {run_name}")
    
    # Log the LangChain agent model
    logged_agent_info = mlflow.pyfunc.log_model(
      artifact_path="agent",
      python_model=CODE_PATH,
      code_paths=["src"],
      pip_requirements=["-r requirements.txt"],
    )

    print(f"Registering model to Unity Catalog: {FULL_UC_MODEL_NAME}")
    uc_registered_model_info = mlflow.register_model(
      model_uri=logged_agent_info.model_uri, 
      name=FULL_UC_MODEL_NAME
    )

  print(f"Deploying model version {uc_registered_model_info.version} to endpoint: {ENDPOINT_NAME}")
  agents.deploy(
    endpoint_name=ENDPOINT_NAME,
    model_name=FULL_UC_MODEL_NAME,
    model_version=uc_registered_model_info.version,
    deploy_feedback_model=False,
    scale_to_zero=True
  )
  print("Deployment initiated successfully.")

if __name__ == "__main__":
  run_deployment()