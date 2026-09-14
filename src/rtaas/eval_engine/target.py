"""
Target model interface.

Supports any OpenAI-compatible /v1/chat/completions endpoint.
Falls back to a mock response if httpx is not available (for testing).
"""

from __future__ import annotations

import os


class TargetModel:
    """
    Sends prompts to the target LLM via HTTP and returns the text response.

    Args:
        url:   Full URL to a /v1/chat/completions endpoint.
        auth:  Authorization header value (e.g. "Bearer sk-...").
               Falls back to OPENAI_API_KEY env var if not provided.
        model: Model name to pass in the API request body.
    """

    def __init__(
        self,
        url: str,
        auth: str | None = None,
        model: str = "gpt-4o-mini",
        timeout: float = 30.0,
    ) -> None:
        self.url = url
        self.model = model
        self.timeout = timeout
        api_key = auth or os.getenv("OPENAI_API_KEY", "")
        self._headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json",
        }

    def query(self, prompt: str) -> str:
        """Send a single prompt and return the model's text response."""
        try:
            import httpx
        except ImportError:
            return self._mock_response(prompt)

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
        }
        try:
            resp = httpx.post(
                self.url,
                json=payload,
                headers=self._headers,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            return str(resp.json()["choices"][0]["message"]["content"])
        except Exception as exc:
            return f"[ERROR] Target model request failed: {exc}"

    @staticmethod
    def _mock_response(prompt: str) -> str:
        """Deterministic mock for testing without a live API."""
        if "ignore" in prompt.lower() and "instruction" in prompt.lower():
            return "I cannot help with that request."
        if "medication" in prompt.lower() or "dose" in prompt.lower():
            return "Please consult a healthcare professional for medical advice."
        return "This is a mock response for testing purposes."
