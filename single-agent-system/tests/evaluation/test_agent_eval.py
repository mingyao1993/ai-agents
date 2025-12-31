import datetime
import os
import mlflow
from mlflow.genai.scorers import (
    RetrievalGroundedness,
    RelevanceToQuery,
    Safety,
    Guidelines,
)
from mlflow.types.responses import ResponsesAgentRequest

from core.config import settings
from agent_system import mlflow_agent_system

# --- Configuration ---

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
mlflow.set_registry_uri(settings.MLFLOW_REGISTRY_URI)
mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_PATH)

EVAL_DATASET_NAME = (
    f"{settings.UC_CATALOG}.{settings.UC_SCHEMA}.cybersecurity_agent_eval"
)

# --- LLM Judges ---
CYBERSECURITY_REPORT_JUDGES = [
    RetrievalGroundedness(),
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
    RelevanceToQuery(),
    Safety(),
]


# --- Helper Functions ---
def predict_fn(content: str) -> str:
    """Wrapper for agent prediction to be used by mlflow.evaluate."""
    response = mlflow_agent_system.predict(
        ResponsesAgentRequest(input=[{"role": "user", "content": content}])
    )
    return response


def test_run_evaluation():
    """Executes the evaluation pipeline."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"eval_pipeline_run_{timestamp}"

    eval_requests = [
        {"inputs": {"content": "Investigate the following IP Address: 1.1.1.1"}},
        {"inputs": {"content": "Investigate the following IP Address: 3.92.45.47"}},
    ]

    with mlflow.start_run(run_name=run_name) as run:
        eval_results = mlflow.genai.evaluate(
            data=eval_requests,
            predict_fn=predict_fn,
            scorers=CYBERSECURITY_REPORT_JUDGES,
        )
        
        assert eval_results is not None
        assert hasattr(eval_results, "metrics")
