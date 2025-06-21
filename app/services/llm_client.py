# app/services/llm_client.py

from abc import ABC, abstractmethod
from typing import Dict, Any

from .base import LLMClient

class LLMClient(ABC):
    """
    Abstract base class for an LLM client.
    Defines the interface that all concrete LLM clients must implement.
    """

    @abstractmethod
    def summarize_alert(self, alert_data: Dict[str, Any]) -> str:
        """
        Generate a summary for the given alert data.
        """
        pass


class MockLLMClient(LLMClient):
    def summarize_alert(self, alert: dict) -> str:
        source = alert.get("source", "unknown")
        alert_name = alert.get("alert", "NoAlertName")
        labels = alert.get("labels", {})
        instance = labels.get("instance", "unknown")
        severity = labels.get("severity", "info")

        return (
            f"[MOCK] {severity.upper()} alert '{alert_name}' detected on instance "
            f"'{instance}' from source '{source}'. This is a generated summary."
        )

