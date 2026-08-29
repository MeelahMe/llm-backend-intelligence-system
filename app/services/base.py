# app/services/base.py

from abc import ABC, abstractmethod
from typing import Dict


class LLMClient(ABC):
    @abstractmethod
    def summarize_alert(self, alert: Dict) -> str:
        """
        Generate a summary for the given alert dictionary.
        """
        pass
