from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # LLM Configuration
    LLM_ENDPOINT_NAME: str = "databricks-gpt-oss-120b"
    
    # MLflow Configuration
    MLFLOW_TRACKING_URI: str = "databricks"
    MLFLOW_REGISTRY_URI: str = "databricks-uc"
    MLFLOW_EXPERIMENT_PATH: str = "/Shared/cybersecurity-agent-exp"

    # Unity Catalog Configuration
    UC_CATALOG: str = "workspace"
    UC_SCHEMA: str = "default"
    UC_MODEL_NAME: str = "cybersecurity_agent"

    # Agent Configuration
    EXTERNALLY_SERVED_AGENTS: list = []
    IN_CODE_AGENTS: list = []
    TOOLS: list = []

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
