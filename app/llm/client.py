import json
import urllib.request

from app.config import Settings


class LLMClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, prompt: str) -> str:
        request_body = json.dumps({
            "model": self.settings.llm_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
        }).encode("utf-8")
        request = urllib.request.Request(
            f"{self.settings.llm_base_url.rstrip('/')}/chat/completions",
            data=request_body,
            headers={"Authorization": f"Bearer {self.settings.llm_api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.settings.llm_timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload["choices"][0]["message"]["content"]

    def generate_json(self, prompt: str) -> dict:
        content = self.generate(prompt).strip()
        if content.startswith("```"):
            content = content.strip("`").removeprefix("json").strip()
        return json.loads(content)