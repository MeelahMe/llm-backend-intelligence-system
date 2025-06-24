from typing import Dict


class PromptBuilder:
    """
    Handles prompt template construction and versioning.
    This abstraction supports structured prompt engineering
    for reuse, testing, and advanced patterns.
    """

    @staticmethod
    def build_alert_summary_prompt(alert: Dict) -> str:
        """
        Constructs a prompt to summarize an infrastructure alert.

        Args:
            alert (Dict): The incoming alert object with keys like 'source', 'alert',
                          'labels', and 'annotations'.

        Returns:
            str: A formatted prompt string for the LLM.
        """

        source = alert.get("source", "unknown")
        name = alert.get("alert", "unnamed alert")

        labels = alert.get("labels", {})
        instance = labels.get("instance", "unknown instance")
        severity = labels.get("severity", "unknown severity")

        annotations = alert.get("annotations", {})
        description = annotations.get("description", "No description provided.")

        # Future-proofing with explicit formatting
        prompt = (
            f"You are a senior SRE assistant. Summarize the following infrastructure alert:\n\n"
            f"Source: {source}\n"
            f"Alert: {name}\n"
            f"Instance: {instance}\n"
            f"Severity: {severity}\n"
            f"Description: {description}\n\n"
            f"Respond with a single, human-readable summary."
        )

        return prompt
