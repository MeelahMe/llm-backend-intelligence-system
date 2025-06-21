from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="LLM Backend Intelligence System")


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return JSONResponse(content={"status": "ok"})
