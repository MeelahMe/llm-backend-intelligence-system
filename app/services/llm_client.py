import os
from typing import List, Dict


class LLMClient:
    """
    LLMClient provides an abstraction for generating summaries using a language model.
    It supports a mock mode for development and testing to avoid external API usage and costs.
    """

    def __init__(self):
        # Read toggle from environment variable (default to True for safety)
        self.use_mock = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

    def generate_summary(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a summary based on the input conversation messages.

        Args:
            messages (List[Dict[str, str]]): A list of messages, each containing a 'role' and 'content'.

        Returns:
            str: The generated summary (mock or real depending on environment).
        """
        if self.use_mock:
            return self._generate_mock_summary(messages)

        # Placeholder for real LLM integration (e.g., OpenAI, Gemini, Claude)
        return self._generate_real_summary(messages)

    def _generate_mock_summary(self, messages: List[Dict[str, str]]) -> str:
        """
        Mock summary generator for testing and development.

        Args:
            messages (List[Dict[str, str]]): Input conversation messages.

        Returns:
            str: A mock summary response.
        """
        return "This is a mock summary for testing purposes."

    def _generate_real_summary(self, messages: List[Dict[str, str]]) -> str:
        """
        Stub for real LLM call. Replace this with actual integration.

        Args:
            messages (List[Dict[str, str]]): Input conversation messages.

        Returns:
            str: The LLM-generated summary (once implemented).
        """
        # Example: Call to OpenAI ChatCompletion or Gemini
        raise NotImplementedError("Real LLM integration is not yet implemented.")
