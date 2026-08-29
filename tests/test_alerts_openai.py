import os
from fastapi.testclient import TestClient
import pytest

from app.main import app

print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("USE_MOCK_LLM:", os.getenv("USE_MOCK_LLM"))

client = TestClient(app)

# Explicitly force OpenAI LLM for this test
os.environ["USE_MOCK_LLM"] = "false"
os.environ["LLM_PROVIDER"] = "openai"


@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY", "").startswith("sk-xxxx")
    or os.getenv("USE_MOCK_LLM", "").lower() == "true",
    reason="Skipping real OpenAI API test unless a valid key is set and USE_MOCK_LLM is false",
)
def test_openai_llm_create_alert():
    payload = {
        "source": "prometheus",
        "alert": "HighCPUUsage",
        "labels": {"instance": "web-01", "severity": "critical"},
        "annotations": {"description": "CPU usage above 90% for 5 minutes"},
    }

    response = client.post("/alerts/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)
    assert "token_usage" in data
    assert isinstance(data["token_usage"], dict)
    assert "cost_usd" in data
    assert isinstance(data["cost_usd"], float)
