from core.tools import check_ip_reputation, get_current_time
from datetime import datetime

def test_check_ip_reputation_known():
    ip = "8.8.8.8"
    result = check_ip_reputation.invoke(ip)
    assert result["data"]["ipAddress"] == "8.8.8.8"
    assert result["data"]["isp"] == "Google LLC"

def test_check_ip_reputation_unknown():
    ip = "1.2.3.4"
    result = check_ip_reputation.invoke(ip)
    assert "not in database" in result["data"]

def test_get_current_time():
    result = get_current_time.invoke({})
    assert isinstance(datetime.fromisoformat(result), datetime)
