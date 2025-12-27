# Determine Databricks resources to specify for automatic auth passthrough at deployment time
import mlflow
from agent import EXTERNALLY_SERVED_AGENTS, LLM_ENDPOINT_NAME, TOOLS, Genie
from databricks_langchain import UnityCatalogTool, VectorSearchRetrieverTool
from mlflow.models.resources import (
    DatabricksFunction,
    DatabricksGenieSpace,
    DatabricksServingEndpoint,
)
from pkg_resources import get_distribution

# TODO: Manually include underlying resources if needed. See the TODO in the markdown above for more information.
resources = [DatabricksServingEndpoint(endpoint_name=LLM_ENDPOINT_NAME)]
# TODO: Add SQL Warehouses and delta tables powering the Genie Space
# resources.append(DatabricksSQLWarehouse(warehouse_id="<your_warehouse_id>"))
# resources.append(DatabricksTable(table_name="<your_catalog>.<schema>.<table_name>"))

# Add tools from Unity Catalog
for tool in TOOLS:
    if isinstance(tool, VectorSearchRetrieverTool):
        resources.extend(tool.resources)
    elif isinstance(tool, UnityCatalogTool):
        resources.append(DatabricksFunction(function_name=tool.uc_function_name))

# Add serving endpoints and Genie Spaces
for agent in EXTERNALLY_SERVED_AGENTS:
    if isinstance(agent, Genie):
        resources.append(DatabricksGenieSpace(genie_space_id=agent.space_id))
    else:
        resources.append(DatabricksServingEndpoint(endpoint_name=agent.endpoint_name))

with mlflow.start_run():
    logged_agent_info = mlflow.pyfunc.log_model(
        name="agent",
        python_model="agent.py",
        resources=resources,
        pip_requirements=[
            f"databricks-connect=={get_distribution('databricks-connect').version}",
            f"mlflow=={get_distribution('mlflow').version}",
            f"databricks-langchain=={get_distribution('databricks-langchain').version}",
            f"langgraph=={get_distribution('langgraph').version}",
            f"langgraph-supervisor=={get_distribution('langgraph-supervisor').version}",
        ],
    )