class MockLLMClient:
    def summarize_alert(self, source: str, alert: str, labels: dict, annotations: dict) -> dict:
        summary = (
            f"[MOCK] {labels.get('severity', '').upper()} alert "
            f"'{alert}' detected on instance '{labels.get('instance', '')}' "
            f"from source '{source}'. This is a generated summary."
        )

        return {
            "summary": summary,
            "token_usage": {
                "prompt_tokens": 40,
                "completion_tokens": 30,
                "total_tokens": 70
            },
            "cost_usd": 0.0007
        }
