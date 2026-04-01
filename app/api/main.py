from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging


configure_logging()

app = FastAPI(
    title="Ranepa Admission Bot API",
    version="0.1.0",
    debug=settings.DEBUG,
)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def readiness() -> dict[str, str]:
    return {"status": "ready"}
