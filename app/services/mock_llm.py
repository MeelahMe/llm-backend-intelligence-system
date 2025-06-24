class MockLLMClient:
    def summarize_alert(self, alert_data: dict) -> dict:
        summary = (
            f"[MOCK] {alert_data['labels'].get('severity', '').upper()} alert "
            f"'{alert_data['alert']}' detected on instance '{alert_data['labels'].get('instance', '')}' "
            f"from source '{alert_data['source']}'. This is a generated summary."
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
