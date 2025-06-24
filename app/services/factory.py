from app.config.settings import settings


def get_llm_client():
    """
    Factory function to return the appropriate LLM client based on settings.
    """

    if settings.use_mock_llm or settings.llm_provider == "mock":
        from app.services.mock_llm import MockLLMClient
        return MockLLMClient()

    elif settings.llm_provider == "openai":
        from app.services.openai_llm import OpenAILLMClient
        return OpenAILLMClient(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=settings.openai_temperature,
            timeout=settings.openai_timeout,
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
