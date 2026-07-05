"""
LLM Service

Centralized interface for communicating with the LLM.
All agents use this module instead of directly calling the API.
"""

from __future__ import annotations

import json
import logging
from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    APIStatusError,
)

from config import (
    GROK_API_KEY,
    GROK_MODEL,
)

logger = logging.getLogger(__name__)


class LLMService:
    """
    Centralized LLM interface.

    Every AI agent (Planner, Writer, Reviewer)
    communicates with the LLM through this class.
    """

    def __init__(self) -> None:
        """Initialize the Grok client."""

        self.client: OpenAI | None = None

    def _get_client(self) -> OpenAI:
        """
        Create the OpenAI-compatible Grok client only when needed.

        Delaying initialization keeps imports, tests, and the Streamlit app
        usable even before the API key is configured.
        """

        if self.client is not None:
            return self.client

        if not GROK_API_KEY:
            raise ValueError(
                "GROK_API_KEY is not configured. Please check your .env file."
            )

        self.client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=GROK_API_KEY,
        )

        return self.client

    def generate_text(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a text response from the LLM.

        Returns:
            str: Generated response.
        """

        try:
            response = self._get_client().chat.completions.create(
                model=GROK_MODEL,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )

            return response.choices[0].message.content or ""

        except ValueError as exc:
            logger.warning("LLM request skipped: %s", exc)
            return ""

        except (
            APITimeoutError,
            APIConnectionError,
            APIStatusError,
        ):
            logger.exception("LLM request failed.")
            return ""

    def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:
        """
        Generate and parse JSON output from the LLM.

        Returns:
            dict: Parsed JSON response.
        """

        text = self.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0,
        )

        if not text:
            return {}

        try:
            return json.loads(_clean_json_text(text))

        except json.JSONDecodeError:
            logger.warning("LLM returned invalid JSON.")
            return {}

    def health_check(self) -> bool:
        """
        Verify that the LLM is reachable.

        Returns:
            bool: True if successful.
        """

        reply = self.generate_text(
            system_prompt="You are a helpful assistant.",
            user_prompt="Reply with exactly the word OK.",
            max_tokens=5,
        )

        return reply.strip().upper() == "OK"


# Singleton instance used throughout the project
llm = LLMService()


def _clean_json_text(text: str) -> str:
    """
    Clean common LLM JSON formatting before parsing.
    """

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start != -1 and end != -1:
        return cleaned[start : end + 1]

    return cleaned


def call_llm(prompt: str) -> str:
    """
    Backward-compatible helper used by the existing smoke test script.
    """

    return llm.generate_text(
        system_prompt="You are a helpful assistant.",
        user_prompt=prompt,
    )
