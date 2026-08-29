from typing import Optional

from fastapi import Header, HTTPException, status

from app.config.settings import settings


def verify_api_key(x_api_key: Optional[str] = Header(None)) -> None:
    """
    FastAPI dependency that requires a valid X-API-Key header.
    Fails closed: if no API_KEY is configured on the server, every
    request is rejected rather than silently letting everything through.
    The header itself is optional at the FastAPI level so a missing key
    returns our own 401, not FastAPI's default 422 validation error.
    """
    if not settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfiguration: API_KEY not set",
        )
    if x_api_key is None or x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
