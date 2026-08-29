from pydantic import BaseModel
from typing import Optional, Dict


class AlertResponse(BaseModel):
    summary: str
    token_usage: Optional[Dict[str, int]] = None
    cost_usd: Optional[float] = None
