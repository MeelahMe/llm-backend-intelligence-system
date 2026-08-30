import os
from fastapi.testclient import TestClient
import pytest

from app.config.settings import settings
from app.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-API-Key": settings.api_key}

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

    response = client.post("/alerts/", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200

    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)
    # The real OpenAI client does not populate token/cost tracking - only
    # the mock client does. These fields are present (via AlertResponse)
    # but null, not missing.
    assert data["token_usage"] is None
    assert data["cost_usd"] is None
