"""Optional local Ollama client utilities.

The default benchmark uses deterministic execution so tests are reproducible and
safe. This helper is provided for users who want to adapt the repository to a
local Ollama experiment. It is not invoked by default.
"""

from __future__ import annotations

import json
from typing import Any

import requests


class OllamaClient:
    def __init__(self, base_url: str = "http://127.0.0.1:11434", timeout: int = 240):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, model: str, prompt: str, temperature: float = 0.0, max_tokens: int = 256) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature, "num_predict": max_tokens},
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        return str(payload.get("response", ""))

    @staticmethod
    def try_parse_json(text: str) -> dict[str, Any]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw_response": text}
