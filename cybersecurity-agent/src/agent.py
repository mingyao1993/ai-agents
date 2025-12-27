import json
from typing import Generator

import mlflow

from config import LLM_ENDPOINT_NAME
from databricks_langchain import ChatDatabricks
from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph
from mlflow.pyfunc import ResponsesAgent
from mlflow.types.responses import (
    ResponsesAgentRequest,
    ResponsesAgentResponse,
    ResponsesAgentStreamEvent,
    output_to_responses_items_stream,
    to_chat_completions_input,
)
from prompts import INVESTIGATION_AGENT_PROMPT
from tools import check_ip_reputation


class LangGraphResponsesAgent(ResponsesAgent):
    def __init__(self, agent: CompiledStateGraph):
        self.agent = agent

    def predict(self, request: ResponsesAgentRequest) -> ResponsesAgentResponse:
        outputs = [
            event.item
            for event in self.predict_stream(request)
            if event.type == "response.output_item.done"
        ]
        return ResponsesAgentResponse(
            output=outputs, custom_outputs=request.custom_inputs
        )

    def predict_stream(
        self,
        request: ResponsesAgentRequest,
    ) -> Generator[ResponsesAgentStreamEvent, None, None]:
        cc_msgs = to_chat_completions_input([i.model_dump() for i in request.input])
        print("This is request.input:", request.input)
        print("This is cc_msgs:", cc_msgs)
        first_message = True
        seen_ids = set()

        # can adjust `recursion_limit` to limit looping: https://docs.langchain.com/oss/python/langgraph/GRAPH_RECURSION_LIMIT#troubleshooting
        for _, events in self.agent.stream(
            {"messages": cc_msgs}, stream_mode=["updates"]
        ):
            new_msgs = [
                msg
                for v in events.values()
                for msg in v.get("messages", [])
                if msg.id not in seen_ids
            ]
            print("this is new msgs:", new_msgs)
            if first_message:
                seen_ids.update(msg.id for msg in new_msgs[: len(cc_msgs)])
                new_msgs = new_msgs[len(cc_msgs) :]
                first_message = False
            else:
                seen_ids.update(msg.id for msg in new_msgs)
                node_name = tuple(events.keys())[0]  # assumes one name per node
                yield ResponsesAgentStreamEvent(
                    type="response.output_item.done",
                    item=self.create_text_output_item(
                        text=f"<name>{node_name}</name>", id=str(uuid4())
                    ),
                )
            if len(new_msgs) > 0:

                def format_msg_content(msg):
                    if isinstance(msg.content, str):
                        try:
                            msg.content = json.loads(msg.content)
                            for item in msg.content:
                                if item.get("type") == "text":
                                    msg.content = item["text"]
                                    break
                        except (json.JSONDecodeError, TypeError):
                            pass
                    return msg

                new_msgs = [format_msg_content(msg) for msg in new_msgs]
                yield from output_to_responses_items_stream(new_msgs)


model = ChatDatabricks(endpoint=LLM_ENDPOINT_NAME)

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

    # Test run
    test_messages = {
        "input":
        # {
        # "role": "user",
        # "content": """
        # Investigate the following indicators of compromise:
        # - IP Address: 192.168.1.1
        # - File Hash: abc123def456
        # """,
        # }
        [
            {
                "role": "user",
                "content": "Hi",
            }
        ]
    }

    # response = agent.invoke(test_messages)
    # print(response)
    # for chunk in agent.stream(test_messages):
    #     # print(pretty_print_messages(chunk))
    #     print(chunk)
    print(mlflow_agent.predict(test_messages))
