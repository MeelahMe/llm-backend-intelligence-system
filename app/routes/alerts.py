from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.schemas.alert import AlertRequest
from app.services.factory import get_llm_client

router = APIRouter()
llm = get_llm_client()

@router.post("/alerts/", status_code=status.HTTP_200_OK)
async def create_alert(alert: AlertRequest):
    """
    Receive an alert and generate a summarized response using LLM.
    Automatically validates incoming request using Pydantic schema.
    """
    try:
        result = llm.summarize_alert(alert.model_dump())

        if isinstance(result, dict):
            summary = result.get("summary")
            token_usage = result.get("token_usage")
            cost = result.get("cost_usd")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "summary": summary,
                    "token_usage": token_usage,
                    "cost_usd": cost
                }
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"summary": result}
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
