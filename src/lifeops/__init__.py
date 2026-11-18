from lifeops.config import get_settings


def main() -> None:
    settings = get_settings()

    print(f"LifeOps running in {settings.environment} mode")
    print(f"LLM provider: {settings.llm_provider}")