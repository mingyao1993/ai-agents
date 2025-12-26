from langchain.tools import tool
from langchain.agents import create_agent
from databricks_langchain import ChatDatabricks
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy


from agents.prompts import INVESTIGATION_AGENT_PROMPT

LLM_ENDPOINT_NAME = "databricks-gpt-oss-20b"
model = ChatDatabricks(endpoint=LLM_ENDPOINT_NAME)

from langchain_google_genai import ChatGoogleGenerativeAI
# model = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
# )

class AbuseIPDBResponse(BaseModel):
    ipAddress: str = Field(..., description="The IP address being queried.")
    isValid: bool = Field(..., description="Indicates if the IP address is valid.")
    abuseConfidenceScore: int = Field(..., description="Abuse confidence score from 0 to 100.")
    countryCode: str = Field(..., description="Country code of the IP address.")
    usageType: str = Field(..., description="Type of usage for the IP address.")

@tool
def check_ip_reputation(ip: str) -> dict:
    """
    Checks the reputation and validity of an IP address using AbuseIPDB data.

    Args:
        ip (str): The IP address to validate.

    Returns:
        dict: The response from the AbuseIPDB API.
    """

    if ip == "118.25.6.39":
        return {
            "data": {
                "ipAddress": "118.25.6.39",
                "isPublic": True,
                "ipVersion": 4,
                "isWhitelisted": False,
                "abuseConfidenceScore": 100,
                "countryCode": "CN",
                "countryName": "China",
                "usageType": "Data Center/Web Hosting/Transit",
                "isp": "Tencent Cloud Computing (Beijing) Co. Ltd",
                "domain": "tencent.com",
                "hostnames": [],
                "isTor": False,
                "totalReports": 1,
                "numDistinctUsers": 1,
                "lastReportedAt": "2018-12-20T20:55:14+00:00",
                "reports": [
                    {
                        "reportedAt": "2018-12-20T20:55:14+00:00",
                        "comment": "Dec 20 20:55:14 srv206 sshd[13937]: Invalid user oracle from 118.25.6.39",
                        "categories": [18, 22],
                        "reporterId": 1,
                        "reporterCountryCode": "US",
                        "reporterCountryName": "United States",
                    }
                ],
            }
        }
    else:
        return {
            "ipAddress": ip,
            "isValid": False,
            "abuseConfidenceScore": 100,
            "countryCode": "Unknown",
            "usageType": "Unknown",
        }


agent = create_agent(
    model,
    tools=[check_ip_reputation],
    system_prompt=INVESTIGATION_AGENT_PROMPT,
)

def create_custom_agent():
    return agent
custom_agent = agent

if __name__ == "__main__":
    from utils.format_messages import pretty_print_messages

    # Test run
    test_messages = {
        "messages": [
            # {
            # "role": "user",
            # "content": """
            # Investigate the following indicators of compromise:
            # - IP Address: 192.168.1.1
            # - File Hash: abc123def456
            # """,
            # }
            {
            "role": "user",
            "content": "Hi",
            }
        ]
    }
    response = agent.invoke(test_messages)
    print(response)
    # for chunk in agent.stream(test_messages):
    #     # print(pretty_print_messages(chunk))
    #     print(chunk)
