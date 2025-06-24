from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from app.schemas.alert import Alert
from app.schemas.response import AlertResponse
from app.services.factory import get_llm_client

router = APIRouter()
llm = get_llm_client()

@router.post("/alerts/", response_model=AlertResponse, status_code=status.HTTP_200_OK)
async def create_alert(request: Request):
    """
    Receive an alert and generate a summarized response using LLM.
    """
    try:
        alert_data = await request.json()
        result = llm.summarize_alert(alert_data)

        if isinstance(result, dict):
            return {
                "summary": result.get("summary"),
                "token_usage": result.get("token_usage"),
                "cost_usd": result.get("cost_usd")
            }

        return {"summary": result}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
