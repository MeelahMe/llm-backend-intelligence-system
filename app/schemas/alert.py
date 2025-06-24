from pydantic import BaseModel
from typing import Dict, Optional

class Alert(BaseModel):
    source: str
    alert: str
    labels: Dict[str, str]
    annotations: Optional[Dict[str, str]] 
