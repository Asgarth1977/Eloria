# llm_client Connections.
# We put here, everything that needs to be, for connection to any llm model.

# -------------------------------
# LiteLLM Client
# -------------------------------
import requests
from config import LITELLM_API_KEY, LITELLM_URL


class LiteLLMClient:
    def __init__(self, api_key=LITELLM_API_KEY, url=LITELLM_URL):
        self.api_key = api_key
        self.url = url

    def send_text(self, text):
        payload = {
            "model": "Eloria",
            "messages": [{"role": "user", "content": text}]
        }
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.post(self.url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json().get("choices", [{}])[0].get("message", {}).get("content", "[No response]")
        except Exception as e:
            return f"[Error from LiteLLM: {e}]"