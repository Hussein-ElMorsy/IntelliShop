from typing import Literal
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.config import get_settings


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    application: str
    version: str
    environment: str


@router.get(
    "",
    response_model=HealthResponse,
    summary="Check application health",
)
def check_health() -> HealthResponse:
    settings = get_settings()

    return HealthResponse(
        status="healthy",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )