from databricks_langchain import ChatDatabricks
from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from core.config import settings
from core.prompts import INVESTIGATION_AGENT_PROMPT
from core.tools import check_ip_reputation, get_current_time


def create_agent_system() -> CompiledStateGraph:
    """
    Factory function to create the cybersecurity investigation agent.
    """
    model = ChatDatabricks(endpoint=settings.DBX_LLM_ENDPOINT_NAME)

    tools = [check_ip_reputation, get_current_time]

    agent_system = create_agent(
        model,
        tools=tools,
        system_prompt=INVESTIGATION_AGENT_PROMPT,
    )

    return agent_system
