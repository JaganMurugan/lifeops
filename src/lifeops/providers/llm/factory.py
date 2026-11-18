
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from lifeops.config import Settings, get_settings


def get_chat_model(
    settings: Settings | None = None,
) -> BaseChatModel:
    """Create a chat model based on the configured LLM provider."""

    if settings is None:
        settings = get_settings()

    if settings.llm_provider == "openai":
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
        )

    if settings.llm_provider == "ollama":
        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
        )

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )
