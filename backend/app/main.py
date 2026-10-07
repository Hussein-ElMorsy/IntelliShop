from fastapi import FastAPI
from app.api.router import api_router 
from app.core.config import get_settings
from app.core.lifespan import lifespan


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "An AI-powered e-commerce platform demonstrating "
        "backend and AI engineering."
    ),
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(
    api_router,
    prefix="/api/v1"
    )


@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    return {
        "message": "Welcome to IntelliShop",
        "documentation": "/docs",
        "health": "/api/v1/health",
    }