
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import model_validator

from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="LIFEOPS_",
        extra="ignore",
    )

    environment: Literal["development", "production", "testing"] = "development"

    llm_provider: Literal["openai", "ollama"] = "ollama"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma4:e2b"

    @model_validator(mode="after")
    def validate_provider_credentials(self):
        if (
            self.llm_provider == "openai"
            and not self.openai_api_key
        ):
            raise ValueError(
                "LIFEOPS_OPENAI_API_KEY is required "
                "when using the OpenAI provider."
            )

        return self

@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()