from google import genai
from google.genai import types

from app.core.config import settings


class GeminiLLMClient:
    def __init__(self, model: str | None = None):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = model or settings.GEMINI_MODEL

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_mime_type: str | None = None,
    ) -> str:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        config = types.GenerateContentConfig(
            temperature=0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )

        if response_mime_type:
            config.response_mime_type = response_mime_type

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
            config=config,
        )

        text = getattr(response, "text", None)
        if not text:
            raise ValueError(f"Empty Gemini response: {response}")

        return text.strip()
