from __future__ import annotations

import time

from google import genai
from google.genai import types

class GemmaProvider:
    """Fast visual identification through hosted Gemma, with one transient-error retry."""

    def __init__(self, api_key: str, model: str, attempt_timeout_seconds: int) -> None:
        self.client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=attempt_timeout_seconds * 1000))
        self.model = model
        self.attempt_timeout_seconds = attempt_timeout_seconds

    def identify(self, image_bytes: bytes, mime_type: str, object_name_override: str | None = None) -> str:
        hint = f"The user says it is a {object_name_override}. Confirm that object." if object_name_override else "Identify the main everyday object."
        config = types.GenerateContentConfig(
            temperature=0,
            max_output_tokens=80,
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.MINIMAL),
        )
        last_error: Exception | None = None
        for attempt in range(1, 3):
            try:
                print(f"[gemma] identify attempt {attempt}/2 | model={self.model!r} | image bytes={len(image_bytes)} | timeout={self.attempt_timeout_seconds}s", flush=True)
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type), f"{hint} Reply with only its common name, using at most three words. If unclear, reply unknown."],
                    config=config,
                )
                text = (response.text or "").strip()
                if not text:
                    raise RuntimeError("Gemma returned an empty response")
                object_name = " ".join(text.replace(".", " ").split()[:3]).lower()
                print(f"[gemma] identify attempt {attempt}/2 succeeded | object={object_name!r}", flush=True)
                return object_name
            except Exception as error:
                last_error = error
                print(f"[gemma] attempt {attempt}/2 failed: {type(error).__name__}: {error}", flush=True)
                if attempt == 1:
                    time.sleep(1.5)
        raise RuntimeError(f"Gemma was unavailable after one retry: {type(last_error).__name__}") from last_error
