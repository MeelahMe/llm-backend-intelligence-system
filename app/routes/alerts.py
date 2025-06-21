# app/routes/alerts.py

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.services.factory import get_llm_client


router = APIRouter()

llm = get_llm_client()  

@router.post("/alerts/", status_code=status.HTTP_200_OK)
async def create_alert(request: Request):
    """
    Receive an alert and generate a summarized response using LLM.
    """
    try:
        alert_data = await request.json()

        # Construct prompt (for now, simple, later modularize)
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes alerts."},
            {"role": "user", "content": f"Summarize this alert: {alert_data}"}
        ]

        summary = llm.generate_summary(messages)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"summary": summary or "LLM did not return a summary."},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )
