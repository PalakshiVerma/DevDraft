import os
import asyncio
import logging
from typing import Optional

from openai import AsyncOpenAI, APIStatusError, APITimeoutError, APIConnectionError

from app.schemas import TaskType, PolishResponse
from app.prompts import get_system_prompt

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config — all driven by environment variables; no provider is hard-coded.
# ---------------------------------------------------------------------------
_LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
_LLM_API_KEY = os.getenv("LLM_API_KEY", "")
_LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
_LLM_FALLBACK_MODEL: Optional[str] = os.getenv("LLM_FALLBACK_MODEL")

# Transient HTTP status codes that warrant a retry
_RETRYABLE_STATUS = {429, 503}
_MAX_RETRIES = 3


def _make_client() -> AsyncOpenAI:
    """Build the async OpenAI-compatible client from env vars."""
    return AsyncOpenAI(
        api_key=_LLM_API_KEY or "ollama",  # Ollama accepts any non-empty key
        base_url=_LLM_BASE_URL,
    )


class PolishService:
    def __init__(self) -> None:
        self._client: Optional[AsyncOpenAI] = None

    @property
    def client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = _make_client()
        return self._client

    def is_configured(self) -> bool:
        """True when an API key is present (not needed for local Ollama)."""
        return bool(_LLM_API_KEY)

    async def _call_model(self, model: str, system: str, user: str) -> str:
        """Single attempt — raises on failure, returns text on success."""
        chat = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        return (chat.choices[0].message.content or "").strip()

    async def _call_with_retry(self, model: str, system: str, user: str) -> str:
        """
        Retry on transient errors (429 / 503 / timeout / connection reset)
        with exponential back-off. Raises immediately on 400/401/403.
        """
        last_exc: Exception = RuntimeError("No attempts made")
        for attempt in range(_MAX_RETRIES):
            try:
                text = await self._call_model(model, system, user)
                if text:
                    return text
                # Empty response treated as transient; retry
            except APIStatusError as exc:
                if exc.status_code not in _RETRYABLE_STATUS:
                    # Non-retryable client error — surface immediately
                    raise ValueError(
                        f"LLM API returned {exc.status_code}: {exc.message}"
                    ) from exc
                last_exc = exc
                logger.warning(
                    "Retryable status %s from model %s (attempt %d/%d)",
                    exc.status_code, model, attempt + 1, _MAX_RETRIES,
                )
            except (APITimeoutError, APIConnectionError) as exc:
                last_exc = exc
                logger.warning(
                    "Transient network error from model %s (attempt %d/%d): %s",
                    model, attempt + 1, _MAX_RETRIES, exc,
                )

            if attempt < _MAX_RETRIES - 1:
                await asyncio.sleep(2 ** attempt)  # 1s, 2s, 4s

        raise RuntimeError(
            f"Model '{model}' failed after {_MAX_RETRIES} attempts."
        ) from last_exc

    async def polish_update(self, raw_text: str, task_type: TaskType) -> PolishResponse:
        system_prompt = get_system_prompt(task_type)
        user_message = f"Here are my raw notes to format:\n\n{raw_text}"

        models_to_try = [_LLM_MODEL]
        if _LLM_FALLBACK_MODEL and _LLM_FALLBACK_MODEL != _LLM_MODEL:
            models_to_try.append(_LLM_FALLBACK_MODEL)

        last_exc: Exception = RuntimeError("No models configured")
        for model in models_to_try:
            try:
                text = await self._call_with_retry(model, system_prompt, user_message)
                return PolishResponse(
                    polished_text=text,
                    task_type=task_type,
                    model_used=model,
                )
            except ValueError:
                # Non-retryable (4xx) — re-raise so caller maps it to 400
                raise
            except RuntimeError as exc:
                last_exc = exc
                logger.error("Model '%s' exhausted retries: %s", model, exc)

        raise RuntimeError(str(last_exc))


polish_service = PolishService()
