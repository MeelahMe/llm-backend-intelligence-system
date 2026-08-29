from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes import alerts

app = FastAPI(title="LLM Backend Intelligence System")

# Register alerts router
app.include_router(alerts.router)


@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(content={"status": "ok"})
