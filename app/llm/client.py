import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class LLMClient:

    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL")
        self.model = os.getenv("LLM_MODEL")

    async def chat(
        self,
        messages: list,
        tools: list | None = None,
    ):

        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            data["tools"] = tools

        async with httpx.AsyncClient() as client:

            response = await client.post(
                url,
                headers=headers,
                json=data,
                timeout=60,
            )

        response.raise_for_status()

        return response.json()