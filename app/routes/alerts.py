from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
import traceback

from app.auth import verify_api_key
from app.rate_limit import limiter
from app.schemas import Alert
from app.services.factory import get_llm_client

router = APIRouter()
llm = get_llm_client()


@router.post("/alerts/", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def create_alert(request: Request, alert: Alert):
    try:
        result = llm.summarize_alert(
            source=alert.source,
            alert=alert.alert,
            labels=alert.labels,
            annotations=alert.annotations,
        )

        # If result is a dict (like from mock), return as-is
        if isinstance(result, dict):
            return result

        # If result is just a string (like from real OpenAI), wrap it
        return {"summary": result}

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": str(e)},
        )
