import os
from typing import Optional
from google import genai
from google.genai import types
from app.schemas import TaskType, PolishResponse
from app.prompts import get_system_prompt

import time

PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-flash-latest"]


class PolishService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._client: Optional[genai.Client] = None

    @property
    def client(self) -> genai.Client:
        if self._client is None:
            current_key = self.api_key or os.getenv("GEMINI_API_KEY")
            if not current_key:
                raise ValueError("GEMINI_API_KEY is not set. Please provide it in environment variables or .env file.")
            self._client = genai.Client(api_key=current_key)
        return self._client

    def is_configured(self) -> bool:
        return bool(self.api_key or os.getenv("GEMINI_API_KEY"))

    async def polish_update(self, raw_text: str, task_type: TaskType) -> PolishResponse:
        system_instruction = get_system_prompt(task_type)
        last_error = None

        # Retry with brief backoff to smoothly absorb temporary 503 high-demand spikes
        for attempt in range(4):
            for model in FALLBACK_MODELS:
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=f"Here are my raw notes to format:\n\n{raw_text}",
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.3,
                            max_output_tokens=1024,
                        ),
                    )
                    polished_text = (response.text or "").strip()
                    if polished_text:
                        return PolishResponse(
                            polished_text=polished_text,
                            task_type=task_type,
                            model_used=model,
                        )
                except Exception as e:
                    last_error = e
                    # If model is unavailable or busy, try next model or wait briefly
                    continue
            time.sleep(1.5 * (attempt + 1))

        raise RuntimeError(f"Gemini API temporary overload. Please retry in a moment. (Details: {str(last_error)})")


polish_service = PolishService()
