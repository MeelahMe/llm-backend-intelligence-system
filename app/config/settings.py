from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # General
    llm_provider: str = Field("mock", env="LLM_PROVIDER")
    use_mock_llm: bool = Field(True, env="USE_MOCK_LLM")

    # OpenAI-specific
    openai_api_key: str = Field("", env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-3.5-turbo", env="OPENAI_MODEL")
    openai_temperature: float = Field(0.3, env="OPENAI_TEMPERATURE")
    openai_timeout: int = Field(10, env="OPENAI_TIMEOUT")

    class Config:
        env_file = ".env"


settings = Settings()
