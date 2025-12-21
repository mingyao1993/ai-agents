from langchain.tools import tool
from langchain.agents import create_agent


from databricks_langchain import ChatDatabricks

LLM_ENDPOINT_NAME = "databricks-gpt-oss-20b"
model = ChatDatabricks(endpoint=LLM_ENDPOINT_NAME)


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
    system_prompt="""
    You are a cybersecurity investigation agent. 
    Your task is to investigate indicators of compromise (IOCs) such as IP addresses, file hashes, and domain names. 
    Use the provided tools to validate and analyze these IOCs.
    """,
)

if __name__ == "__main__":
    from utils.format_messages import pretty_print_messages
    
    # Test run
    test_messages = {
        "messages": [
            {
                "role": "user",
                "content": """
            Investigate the following indicators of compromise:
            - IP Address: 192.168.1.1
            - File Hash: abc123def456
            """,
            }
        ]
    }
    # response = agent.invoke(test_messages)
    for chunk in agent.stream(test_messages):
        print(pretty_print_messages(chunk))
