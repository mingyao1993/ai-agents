import os
import mlflow
from core.config import settings
from mlflow.genai.scorers import (
    RetrievalGroundedness,
    RelevanceToQuery,
    Safety,
    Guidelines,
)

# Save the LLM Judges as a variable so you can re-use them in step 7

cybersecurity_report_judges = [
    RetrievalGroundedness(),  # Checks if email content is grounded in retrieved data
    Guidelines(
        name="follows_instructions",
        guidelines="The generated report must follow the Investigation Guidelines in the request.",
    ),
    Guidelines(
        name="concise_communication",
        guidelines="The report MUST be concise and to the point. The report should communicate the key message efficiently without being overly brief or losing important context.",
    ),
    Guidelines(
        name="report_format",
        guidelines="The generated report MUST follow the specified Response Format in the request e.g. IOC Type & Value, Risk Assessment, Key Findings, Recommended Actions.",
    ),
    Guidelines(
        name="includes_next_steps",
        guidelines="The report MUST end with a specific, actionable next step that includes a concrete timeline.",
    ),
    RelevanceToQuery(),  # Checks if email addresses the user's request
    Safety(),  # Checks for harmful or inappropriate content
]

# read from eval dataset
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
mlflow.set_registry_uri(settings.MLFLOW_REGISTRY_URI)
mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_PATH)

EVAL_DATASET_NAME = f"{settings.UC_CATALOG}.{settings.UC_SCHEMA}.cybersecurity_agent_eval"

os.environ["MLFLOW_GENAI_EVAL_SKIP_TRACE_VALIDATION"] = "True" # causing issues in local dev

dataset = mlflow.genai.datasets.get_dataset(name=EVAL_DATASET_NAME)

def predict_fn(request: dict) -> str:
    from agent_system import mlflow_agent_system
    response = mlflow_agent_system.predict(request)
    return response


# Run evaluation with LLM Judges
eval_results = mlflow.genai.evaluate(
    data=dataset,
    predict_fn=predict_fn,
    scorers=cybersecurity_report_judges,
)
