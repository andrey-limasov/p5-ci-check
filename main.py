import logging

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse

import settings

app = FastAPI(
    title="Project Name",
    description="Project description",
    version="0.3.0",
    # Документация API — только в dev
    docs_url="/docs" if settings.APP_ENV == "dev" else None,
    redoc_url="/redoc" if settings.APP_ENV == "dev" else None,
    openapi_url="/openapi.json" if settings.APP_ENV == "dev" else None,
)

TEAM_NAME = "repair-requests"
logger = logging.getLogger("uvicorn.error")


@app.get("/")
async def root():
    """Root endpoint: проверка, что приложение отвечает."""
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    """Приложение работает и база данных отвечает на запрос."""
    try:
        with psycopg.connect(
            settings.DATABASE_URL, connect_timeout=settings.DB_CONNECT_TIMEOUT
        ) as conn:
            conn.execute("SELECT 1")
    except psycopg.Error as exc:
        logger.warning("Health check: database is unavailable: %s", exc)
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "unavailable"},
        )
    return {"status": "healthy", "database": "ok"}


@app.get("/version")
async def version():
    """Версия приложения и команда-владелец."""
    return {"version": app.version, "team": TEAM_NAME}
