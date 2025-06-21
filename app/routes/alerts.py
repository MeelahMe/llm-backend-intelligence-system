from fastapi import APIRouter
from app.models.alert import AlertIn, AlertOut
from app.services.summarizer import generate_mock_summary

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)

@router.post("/", response_model=AlertOut)
def create_alert(alert: AlertIn):
    return generate_mock_summary(alert)
