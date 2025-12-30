import unittest
from core.tools import check_ip_reputation, get_current_time
from datetime import datetime

class TestTools(unittest.TestCase):
    def test_check_ip_reputation_known(self):
        ip = "8.8.8.8"
        result = check_ip_reputation.invoke(ip)
        self.assertEqual(result["data"]["ipAddress"], "8.8.8.8")
        self.assertEqual(result["data"]["isp"], "Google LLC")

    def test_check_ip_reputation_unknown(self):
        ip = "1.2.3.4"
        result = check_ip_reputation.invoke(ip)
        self.assertIn("not in database", result["data"])

    def test_get_current_time(self):
        result = get_current_time.invoke({})
        self.assertIsInstance(datetime.fromisoformat(result),datetime)


if __name__ == "__main__":
    unittest.main()
