# app/services/factory.py

import os
from app.services.llm_client import LLMClient, MockLLMClient

# Future: from app.services.gemini_client import GeminiLLMClient
# Future: from app.services.openai_client import OpenAILLMClient

def get_llm_client() -> LLMClient:
    """
    Factory function to return the appropriate LLM client
    based on environment configuration.
    """
    provider = os.getenv("LLM_PROVIDER", "mock").lower()

    if provider == "mock":
        return MockLLMClient()
    
    # elif provider == "gemini":
    #     return GeminiLLMClient(api_key=os.getenv("GEMINI_API_KEY"))

    # elif provider == "openai":
    #     return OpenAILLMClient(api_key=os.getenv("OPENAI_API_KEY"))

    raise ValueError(f"Unsupported LLM provider: {provider}")
