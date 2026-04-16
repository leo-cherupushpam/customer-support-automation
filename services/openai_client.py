# OpenAI API client with retry logic and monitoring

import os
import time
import logging
from typing import Optional, Any
from openai import OpenAI, RateLimitError, APIError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class OpenAIClient:
    """OpenAI API client with retry logic and monitoring"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        max_tokens: int = 500,
        max_retries: int = 3,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries

        # Metrics
        self.total_calls = 0
        self.total_tokens = 0
        self.error_count = 0

    def chat_completion(
        self,
        messages: list[dict[str, str]],
        response_format: Optional[dict] = None,
        stream: bool = False,
    ) -> Any:
        """Make chat completion with retry logic"""
        self.total_calls += 1

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    response_format=response_format,
                    stream=stream,
                )

                # Track tokens
                if response.usage:
                    self.total_tokens += response.usage.total_tokens

                return response

            except RateLimitError as e:
                wait_time = 2**attempt  # Exponential backoff
                logger.warning(
                    f"Rate limit hit, retrying in {wait_time}s (attempt {attempt + 1})"
                )
                time.sleep(wait_time)

            except APIError as e:
                logger.error(f"API error: {e}")
                self.error_count += 1
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(1)

        raise Exception("Max retries exceeded")

    def get_metrics(self) -> dict:
        """Get API usage metrics"""
        return {
            "total_calls": self.total_calls,
            "total_tokens": self.total_tokens,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.total_calls, 1),
        }
