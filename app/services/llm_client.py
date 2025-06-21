# app/services/llm_client.py

import os
import logging
from typing import Any, Dict, Optional

import openai  

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_summary(self, messages: list[Dict[str, str]]) -> Optional[str]:
        """
        Sends a prompt to the LLM and returns the response.
        Includes basic error handling and logging.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
            )
            summary = response.choices[0].message["content"]
            logger.info("LLM response received.")
            return summary
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return None


