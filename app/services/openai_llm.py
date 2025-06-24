import logging
from openai import OpenAI, OpenAIError

logger = logging.getLogger(__name__)


class OpenAILLMClient:
    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.5,
        max_tokens: int = 100,
        timeout: int = 30
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

        # Pass timeout via configuration (if needed)
        self.client = OpenAI(api_key=api_key, timeout=timeout) if api_key else OpenAI(timeout=timeout)

    def summarize_alert(self, source: str, alert: str, labels: dict, annotations: dict) -> str:
        try:
            message = (
                f"A new alert has been triggered from source '{source}'.\n\n"
                f"**Alert:** {alert}\n"
                f"**Labels:** {labels}\n"
                f"**Annotations:** {annotations}\n\n"
                f"Generate a short human-readable summary in one sentence for this alert."
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an assistant that summarizes monitoring alerts for DevOps teams."},
                    {"role": "user", "content": message}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return response.choices[0].message.content.strip()

        except OpenAIError as e:
            logger.error(f"[OpenAI] Exception: {e}")
            return "[ERROR] Failed to generate summary."


