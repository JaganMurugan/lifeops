
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from lifeops.config import Settings
from lifeops.providers.llm.factory import get_chat_model


def test_factory_creates_ollama_model():
    settings = Settings(
        llm_provider="ollama",
        ollama_model="gemma4:e2b",
        _env_file=None,
    )

    model = get_chat_model(settings)

    assert isinstance(model, ChatOllama)


def test_factory_creates_openai_model():
    settings = Settings(
        llm_provider="openai",
        openai_api_key="test-api-key",
        openai_model="gpt-4.1-mini",
        _env_file=None,
    )

    model = get_chat_model(settings)

    assert isinstance(model, ChatOpenAI)
