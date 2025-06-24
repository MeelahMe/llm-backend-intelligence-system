import os
from app.services.openai_llm import OpenAILLMClient
from app.services.mock_llm import MockLLMClient

def get_llm_client():
    if os.getenv("USE_MOCK_LLM", "").lower() == "true":
        return MockLLMClient()
    return OpenAILLMClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", 0.5)),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", 100)),
        timeout=int(os.getenv("OPENAI_TIMEOUT", 30)),
    )
   