from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("backend/.env", ".env", "../.env"), extra="ignore")
    gemini_api_key: str | None = Field(default=None, validation_alias="GEMINI_API_KEY")
    gemma_model: str = Field(default="gemma-4-26b-a4b-it", validation_alias="GEMMA_MODEL")
    gemma_attempt_timeout_seconds: int = Field(default=45, validation_alias="GEMMA_ATTEMPT_TIMEOUT_SECONDS")
    frontend_origin: str = Field(default="http://localhost:5173", validation_alias="FRONTEND_ORIGIN")
    max_upload_mb: int = Field(default=8, validation_alias="MAX_UPLOAD_MB")
    elevenlabs_api_key: str | None = Field(default=None, validation_alias="ELEVENLABS_API_KEY")
    elevenlabs_voice_id: str = Field(default="pNInz6obpgDQGcFmaJgB", validation_alias="ELEVENLABS_VOICE_ID")


@lru_cache
def get_settings() -> Settings:
    return Settings()
