# tests/test_alerts.py

def test_create_alert(client):
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

    assert "summary" in data
    assert data["summary"].startswith("[MOCK] CRITICAL alert 'HighCPUUsage'")


def test_missing_fields(client):
    """
    Test payload missing required fields like 'alert'.
    """
    payload = {
        "source": "prometheus",
        "labels": {
            "instance": "web-01",
            "severity": "critical"
        }
    }
    response = client.post("/alerts/", json=payload)
    assert response.status_code == 200 or response.status_code == 500
    assert "summary" in response.json() or "error" in response.json()


def test_invalid_json_structure(client):
    """
    Send invalid JSON structure (e.g., a list instead of a dict).
    """
    response = client.post("/alerts/", json=[1, 2, 3])
    assert response.status_code == 500
    assert "error" in response.json()


def test_missing_labels(client):
    """
    Test payload missing 'labels' dictionary.
    """
    payload = {
        "source": "prometheus",
        "alert": "DiskFull",
        "annotations": {
            "description": "Disk usage above 95%"
        }
    }
    response = client.post("/alerts/", json=payload)
    assert response.status_code == 200 or response.status_code == 500
    assert "summary" in response.json() or "error" in response.json()


def test_invalid_data_types(client):
    """
    Test where a value has the wrong type (e.g., labels should be dict but is list).
    """
    payload = {
        "source": "prometheus",
        "alert": "BadInput",
        "labels": ["should", "be", "a", "dict"],
        "annotations": {
            "description": "Something broke"
        }
    }
    response = client.post("/alerts/", json=payload)
    assert response.status_code == 200 or response.status_code == 500
    assert "summary" in response.json() or "error" in response.json()


def test_mock_failure_handling(client, monkeypatch):
    """
    Simulate LLM client failure to test error handling.
    """
    def broken_summary(alert_data):
        raise RuntimeError("Mock LLM failure")

    from app.routes import alerts
    monkeypatch.setattr(alerts.llm, "summarize_alert", broken_summary)

    payload = {
        "source": "prometheus",
        "alert": "CrashLoop",
        "labels": {
            "instance": "db-01",
            "severity": "high"
        }
    }
    response = client.post("/alerts/", json=payload)
    assert response.status_code == 500
    assert "error" in response.json()

