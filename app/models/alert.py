from pydantic import BaseModel, Field
from typing import Dict, Optional


class AlertIn(BaseModel):
    """
    Schema for incoming alert payloads.
    Follows common monitoring formats like Prometheus AlertManager.
    """

    source: str
    alert: str
    labels: Dict[str, str]
    annotations: Optional[Dict[str, str]] = Field(default_factory=dict)


class AlertOut(BaseModel):
    """
    Schema for the API response returned after summarization.
    Includes a unique alert ID and a human-readable summary.
    """

    alert_id: str
    summary: str
