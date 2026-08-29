from fastapi.testclient import TestClient

from app.config.settings import settings
from app.main import app

client = TestClient(app)

PAYLOAD = {
    "source": "prometheus",
    "alert": "HighCPUUsage",
    "labels": {"instance": "web-01", "severity": "critical"},
    "annotations": {"description": "CPU usage above 90% for 5 minutes"},
}


def test_missing_api_key_returns_401():
    response = client.post("/alerts/", json=PAYLOAD)
    assert response.status_code == 401
    assert "detail" in response.json()


def test_wrong_api_key_returns_401():
    response = client.post(
        "/alerts/", json=PAYLOAD, headers={"X-API-Key": "definitely-not-the-real-key"}
    )
    assert response.status_code == 401


def test_correct_api_key_succeeds():
    response = client.post(
        "/alerts/", json=PAYLOAD, headers={"X-API-Key": settings.api_key}
    )
    assert response.status_code == 200
