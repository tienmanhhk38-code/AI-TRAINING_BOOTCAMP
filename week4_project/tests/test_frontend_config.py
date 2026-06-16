import os
import unittest

from frontend.config import get_api_base_url


class FrontendConfigTest(unittest.TestCase):
    def test_api_base_url_defaults_to_current_backend_port(self):
        old_value = os.environ.pop("API_BASE_URL", None)
        try:
            self.assertEqual(get_api_base_url(), "http://127.0.0.1:8002")
        finally:
            if old_value is not None:
                os.environ["API_BASE_URL"] = old_value

    def test_api_base_url_reads_environment_value(self):
        old_value = os.environ.get("API_BASE_URL")
        try:
            os.environ["API_BASE_URL"] = "http://127.0.0.1:9999/"
            self.assertEqual(get_api_base_url(), "http://127.0.0.1:9999")
        finally:
            if old_value is None:
                os.environ.pop("API_BASE_URL", None)
            else:
                os.environ["API_BASE_URL"] = old_value


if __name__ == "__main__":
    unittest.main()
