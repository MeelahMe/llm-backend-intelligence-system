import openai
from app.prompts.prompt_engineering import PromptBuilder


class OpenAILLMClient:
    """
    Handles communication with the OpenAI ChatCompletion API.
    """

    def __init__(self, api_key: str, model: str, temperature: float, timeout: int):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.timeout = timeout

        openai.api_key = self.api_key

    def summarize_alert(self, alert_data: dict) -> dict:
        """
        Summarizes an incoming alert using the configured OpenAI model.

        Returns:
            dict: {
                summary: str,
                token_usage: dict,
                cost_usd: float
            }
        """
        prompt = PromptBuilder.build_alert_summary_prompt(alert_data)

        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": "You are an expert site reliability engineer."},
                {"role": "user", "content": prompt}
            ],
            request_timeout=self.timeout
        )

        summary = response["choices"][0]["message"]["content"].strip()
        usage = response.get("usage", {})

        # Estimate cost if token usage is available
        cost_usd = self._estimate_cost(usage)

        return {
            "summary": summary,
            "token_usage": usage,
            "cost_usd": cost_usd
        }

    def _estimate_cost(self, usage: dict) -> float:
        """
        Estimate the OpenAI cost in USD based on token usage.
        Pricing: https://openai.com/pricing
        """
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        # Prices (USD / 1K tokens)
        if "gpt-4" in self.model:
            prompt_price = 0.03
            completion_price = 0.06
        else:
            prompt_price = 0.0015  # e.g., gpt-3.5-turbo
            completion_price = 0.002

        cost = (
            (prompt_tokens / 1000) * prompt_price
            + (completion_tokens / 1000) * completion_price
        )

        return round(cost, 6)

