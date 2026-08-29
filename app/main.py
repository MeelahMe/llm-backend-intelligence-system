from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routes import alerts
from app.rate_limit import limiter

app = FastAPI(title="LLM Backend Intelligence System")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Register alerts router
app.include_router(alerts.router)


@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(content={"status": "ok"})
