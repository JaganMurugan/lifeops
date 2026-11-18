import pytest
from pydantic import ValidationError

from lifeops.config import Settings

from lifeops.config import get_settings

def clear_lifeops_env(monkeypatch):
    """Remove LifeOps environment variables for isolated tests."""
    variables = [
        "LIFEOPS_ENV",
        "LIFEOPS_LLM_PROVIDER",
        "LIFEOPS_OPENAI_API_KEY",
        "LIFEOPS_OPENAI_MODEL",
        "LIFEOPS_OLLAMA_BASE_URL",
        "LIFEOPS_OLLAMA_MODEL",
    ]

    for variable in variables:
        monkeypatch.delenv(variable, raising=False)


def test_default_settings(monkeypatch):
    clear_lifeops_env(monkeypatch)

    settings = Settings(_env_file=None)

    assert settings.environment == "development"
    assert settings.llm_provider == "ollama"
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.ollama_model == "gemma4:e2b"
    assert settings.openai_api_key is None


def test_environment_variables_override_defaults(monkeypatch):
    clear_lifeops_env(monkeypatch)

    monkeypatch.setenv("LIFEOPS_LLM_PROVIDER", "openai")
    monkeypatch.setenv("LIFEOPS_OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("LIFEOPS_OPENAI_MODEL", "gpt-4.1-mini")

    settings = Settings(_env_file=None)

    assert settings.llm_provider == "openai"
    assert settings.openai_api_key == "test-api-key"
    assert settings.openai_model == "gpt-4.1-mini"


def test_invalid_provider_is_rejected(monkeypatch):
    clear_lifeops_env(monkeypatch)

    monkeypatch.setenv("LIFEOPS_LLM_PROVIDER", "invalid-provider")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_ollama_does_not_require_openai_api_key(monkeypatch):
    clear_lifeops_env(monkeypatch)

    monkeypatch.setenv("LIFEOPS_LLM_PROVIDER", "ollama")

    settings = Settings(_env_file=None)

    assert settings.llm_provider == "ollama"
    assert settings.openai_api_key is None


def test_openai_requires_api_key(monkeypatch):
    clear_lifeops_env(monkeypatch)

    monkeypatch.setenv("LIFEOPS_LLM_PROVIDER", "openai")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)

def test_get_settings_returns_cached_instance(monkeypatch):
    clear_lifeops_env(monkeypatch)
    get_settings.cache_clear()

    first = get_settings()
    second = get_settings()

    assert first is second

    get_settings.cache_clear()