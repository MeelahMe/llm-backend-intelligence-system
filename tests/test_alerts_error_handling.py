from unittest.mock import patch

from fastapi.testclient import TestClient

from app.config.settings import settings
from app.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-API-Key": settings.api_key}

PAYLOAD = {
    "source": "prometheus",
    "alert": "HighCPUUsage",
    "labels": {"instance": "web-01", "severity": "critical"},
    "annotations": {"description": "CPU usage above 90% for 5 minutes"},
}


def test_alert_creation_handles_llm_exception():
    """
    Confirms the except block in create_alert() actually catches and
    reports errors correctly, rather than assuming it works because
    it's never been exercised by a real failure.
    """
    with patch(
        "app.routes.alerts.llm.summarize_alert", side_effect=RuntimeError("boom")
    ):
        response = client.post("/alerts/", json=PAYLOAD, headers=AUTH_HEADERS)

    assert response.status_code == 500
    data = response.json()
    assert data["error"] == "Internal Server Error"
    assert "boom" in data["detail"]
