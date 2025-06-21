from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_alert():
    """
    Test the POST /alerts endpoint with a valid alert payload.
    """
    payload = {
        "source": "prometheus",
        "alert": "HighCPUUsage",
        "labels": {
            "instance": "web-01",
            "severity": "critical"
        },
        "annotations": {
            "description": "CPU usage above 90% for 5 minutes"
        }
    }

    response = client.post("/alerts/", json=payload)

    assert response.status_code == 200
    data = response.json()

    # Assert that the response contains the expected keys and formats
    assert "alert_id" in data
    assert "summary" in data
    assert data["summary"].startswith("🛠️ Alert 'HighCPUUsage'")

