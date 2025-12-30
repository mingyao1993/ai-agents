import datetime
import mlflow
from core.config import settings
from databricks import agents

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
mlflow.set_registry_uri(settings.MLFLOW_REGISTRY_URI)



# Input example used by MLflow to infer Model Signature
input_example = {
  "input": [
    {
      "role": "user",
      "content": "Hi",
    }
  ]
}


### Log the LangChain agent model to MLflow
mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_PATH)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
run_name = f"pipeline_run_{timestamp}"

code_path = "src/agent_system.py"

with mlflow.start_run(run_name=run_name):
  
  logged_agent_info = mlflow.pyfunc.log_model(
    name="agent",
    python_model=code_path,
    code_paths=["src"], # include the src directory to preserve package structure
    pip_requirements=["-r requirements.txt"],
  )

  print(f"MLflow Run: {logged_agent_info.run_id}")
  print(f"Model URI: {logged_agent_info.model_uri}")


# pre-deployment agent validation
print("Validating logged model...")
try:
    mlflow.models.predict(
        model_uri=f"runs:/{logged_agent_info.run_id}/agent",
        input_data=input_example,
        env_manager="uv",
    )
except Exception as e:
    print(f"Validation failed: {e}")


#### Register the model to Unity Catalog after result is satisfactory
print("Registering model to Unity Catalog...")
FULL_UC_MODEL_NAME = f"{settings.UC_CATALOG}.{settings.UC_SCHEMA}.{settings.UC_MODEL_NAME}"

# register the model to UC
uc_registered_model_info = mlflow.register_model(
    model_uri=logged_agent_info.model_uri, 
    name=FULL_UC_MODEL_NAME
)


# Deploy the registered model as a Databricks Agent endpoint
print("Deploying model as Databricks Agent endpoint...")

agents.deploy(
    endpoint_name="cybersecurity-agent-endpoint",
    model_name=FULL_UC_MODEL_NAME,
    model_version=uc_registered_model_info.version,
    deploy_feedback_model=False,
    scale_to_zero=True
)