import mlflow

from config import LLM_ENDPOINT_NAME
from databricks_langchain import ChatDatabricks
from langchain.agents import create_agent
from mlflow_helpers.responses_agent import LangGraphResponsesAgent

from prompts import INVESTIGATION_AGENT_PROMPT
from tools import check_ip_reputation


model = ChatDatabricks(endpoint=LLM_ENDPOINT_NAME)

# import dotenv
# dotenv.load_dotenv()
# from langchain_google_genai import ChatGoogleGenerativeAI
# model = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
# )

mlflow.langchain.autolog()
agent = create_agent(
    model,
    tools=[check_ip_reputation],
    system_prompt=INVESTIGATION_AGENT_PROMPT,
)
mlflow_agent = LangGraphResponsesAgent(agent)
mlflow.models.set_model(mlflow_agent)

if __name__ == "__main__":
    from utils.format_messages import pretty_print_messages

    mlflow.set_tracking_uri("databricks")
    mlflow.set_experiment(
        "/Shared/cybersecurity-agent-exp"
    )  # set experiment. if not exists, it will be created

    # Test run
    prompts = [
        "Investigate the following IP Address: 1.1.1.1",
        "Investigate the following IP Address: 118.25.6.39",
        "Investigate the following IP Address: 127.0.0.1",
        "Investigate the following IP Address: 8.8.8.8",
        "Investigate the following IP Address: 3.92.45.47",
        "Investigate the following IP Address: 45.78.219.226",
    ]
    for prompt in prompts:
        test_messages = {
            "input": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        }
        # response = agent.invoke(test_messages)
        # print(response)
        # for chunk in agent.stream(test_messages):
        #     # print(pretty_print_messages(chunk))
        #     print(chunk)

        mlflow_agent.predict(test_messages)
