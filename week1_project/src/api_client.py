import requests


class ApiClient:
    def __init__(self, base_url, api_key="", timeout=10):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def get_customer(self, customer_id):
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = requests.get(
            f"{self.base_url}/users/{customer_id}",
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
