import os


DEFAULT_API_BASE_URL = "http://127.0.0.1:8002"


def get_api_base_url():
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")
