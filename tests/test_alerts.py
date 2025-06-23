from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_alert():
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
    assert "summary" in data
    assert isinstance(data["summary"], str)

    # Only assert metadata if present
    if "token_usage" in data:
        assert isinstance(data["token_usage"], dict)
        assert "prompt_tokens" in data["token_usage"]
        assert "completion_tokens" in data["token_usage"]
        assert "total_tokens" in data["token_usage"]
        assert isinstance(data["cost_usd"], float)

def test_missing_required_field():
    payload = {
        "source": "prometheus",
        # Missing 'alert' field
        "labels": {
            "instance": "web-01",
            "severity": "critical"
        }
    }

    response = client.post("/alerts/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()


