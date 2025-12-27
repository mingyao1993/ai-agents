import datetime
import mlflow

mlflow.set_tracking_uri("databricks")
mlflow.set_registry_uri("databricks-uc")

code_path = "src/agent.py"

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
mlflow.set_experiment("/Shared/cybersecurity-agent-exp") # set experiment. if not exists, it will be created

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
run_name = f"pipeline_run_{timestamp}"


with mlflow.start_run(run_name=run_name):
  logged_agent_info = mlflow.pyfunc.log_model(
    name="agent",
    python_model=code_path,
  )

  print(f"MLflow Run: {logged_agent_info.run_id}")
  print(f"Model URI: {logged_agent_info.model_uri}")



#### Register the model to Unity Catalog after result is satisfactory
catalog = "workspace"
schema = "default"
model_name = "cybersecurity_agent"
UC_MODEL_NAME = f"{catalog}.{schema}.{model_name}"

# register the model to UC
uc_registered_model_info = mlflow.register_model(
    model_uri=logged_agent_info.model_uri, name=UC_MODEL_NAME
)