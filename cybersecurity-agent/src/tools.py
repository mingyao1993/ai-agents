from langchain.tools import tool


ABUSEIPDB_API_RESPONSES = {
    "118.25.6.39": {
        "data": {
            "ipAddress": "118.25.6.39",
            "isPublic": True,
            "ipVersion": 4,
            "isWhitelisted": False,
            "abuseConfidenceScore": 8,
            "countryCode": "CN",
            "usageType": "Data Center/Web Hosting/Transit",
            "isp": "Tencent Cloud Computing (Beijing) Co., Ltd",
            "domain": "tencent.com",
            "hostnames": [],
            "isTor": False,
            "totalReports": 4,
            "numDistinctUsers": 3,
            "lastReportedAt": "2025-12-25T11:02:21+00:00",
        }
    },
    "127.0.0.1": {
        "data": {
            "ipAddress": "127.0.0.1",
            "isPublic": False,
            "ipVersion": 4,
            "isWhitelisted": False,
            "abuseConfidenceScore": 0,
            "countryCode": None,
            "usageType": "Reserved",
            "isp": None,
            "domain": None,
            "hostnames": ["localhost"],
            "isTor": False,
            "totalReports": 2418,
            "numDistinctUsers": 277,
            "lastReportedAt": "2025-12-27T23:34:47+00:00",
        }
    },
    "8.8.8.8": {
        "data": {
            "ipAddress": "8.8.8.8",
            "isPublic": True,
            "ipVersion": 4,
            "isWhitelisted": True,
            "abuseConfidenceScore": 0,
            "countryCode": "US",
            "usageType": "Content Delivery Network",
            "isp": "Google LLC",
            "domain": "google.com",
            "hostnames": ["dns.google"],
            "isTor": False,
            "totalReports": 143,
            "numDistinctUsers": 55,
            "lastReportedAt": "2025-12-24T09:57:47+00:00",
        }
    },
    "3.92.45.47": {
        "data": {
            "ipAddress": "3.92.45.47",
            "isPublic": True,
            "ipVersion": 4,
            "isWhitelisted": False,
            "abuseConfidenceScore": 100,
            "countryCode": "US",
            "usageType": "Data Center/Web Hosting/Transit",
            "isp": "Amazon Data Services Northern Virginia",
            "domain": "amazon.com",
            "hostnames": ["ec2-3-92-45-47.compute-1.amazonaws.com"],
            "isTor": False,
            "totalReports": 64,
            "numDistinctUsers": 44,
            "lastReportedAt": "2025-12-27T23:37:35+00:00",
        }
    },
    "45.78.219.226": {
        "data": {
            "ipAddress": "45.78.219.226",
            "isPublic": True,
            "ipVersion": 4,
            "isWhitelisted": False,
            "abuseConfidenceScore": 100,
            "countryCode": "SG",
            "usageType": "Data Center/Web Hosting/Transit",
            "isp": "BYTEPLUS",
            "domain": "bytedance.com",
            "hostnames": [],
            "isTor": False,
            "totalReports": 2468,
            "numDistinctUsers": 679,
            "lastReportedAt": "2025-12-27T23:36:26+00:00",
        }
    },
}


@tool
def check_ip_reputation(ip: str) -> dict:
    """
    Checks the reputation and validity of an IP address using AbuseIPDB data.
    A rating of 100 means we are sure an IP address is malicious, while a rating of 0 means we have no reason to suspect it is malicious.

    Args:
        ip (str): The IP address to validate.

    Returns:
        dict: The response from the AbuseIPDB API.
    """
    if ip in ABUSEIPDB_API_RESPONSES.keys():
        return ABUSEIPDB_API_RESPONSES[ip]
    else:
        return "IP address not in database."

