import mlflow

from config import LLM_ENDPOINT_NAME
from databricks_langchain import ChatDatabricks
from langchain.agents import create_agent
from mlflow_helpers.responses_agent import LangGraphResponsesAgent

from prompts import INVESTIGATION_AGENT_PROMPT
from tools import check_ip_reputation


model = ChatDatabricks(endpoint=LLM_ENDPOINT_NAME)

# from langchain_google_genai import ChatGoogleGenerativeAI
# model = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
# )

# Set Databricks as the tracking server
# mlflow.set_tracking_uri("databricks")
# mlflow.set_registry_uri("databricks-uc")

mlflow.langchain.autolog()
agent = create_agent(
    model,
    tools=[check_ip_reputation],
    system_prompt=INVESTIGATION_AGENT_PROMPT,
)
mlflow_agent = LangGraphResponsesAgent(agent)
mlflow.models.set_model(mlflow_agent)

# if __name__ == "__main__":
#     from utils.format_messages import pretty_print_messages

#     # Test run
#     test_messages = {
#         "input":
#         # {
#         # "role": "user",
#         # "content": """
#         # Investigate the following indicators of compromise:
#         # - IP Address: 192.168.1.1
#         # - File Hash: abc123def456
#         # """,
#         # }
#         [
#             {
#                 "role": "user",
#                 "content": "Hi",
#             }
#         ]
#     }

#     # response = agent.invoke(test_messages)
#     # print(response)
#     # for chunk in agent.stream(test_messages):
#     #     # print(pretty_print_messages(chunk))
#     #     print(chunk)
#     print(mlflow_agent.predict(test_messages))
