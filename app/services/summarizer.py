import uuid
from app.models.alert import AlertIn, AlertOut


def generate_mock_summary(alert: AlertIn) -> AlertOut:
    """
    Simulates alert summarization by generating a human-readable message.
    This function is a placeholder and will later be replaced with an actual LLM integration.
    """
    instance = alert.labels.get("instance", "unknown")
    summary = (
        f"🛠️ Alert '{alert.alert}' triggered from {alert.source}. "
        f"Suggested next step: investigate '{instance}'."
    )
    return AlertOut(alert_id=str(uuid.uuid4()), summary=summary)
