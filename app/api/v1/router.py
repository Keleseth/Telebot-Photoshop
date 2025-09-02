from fastapi import APIRouter
from app.config import settings
from app.api.v1.endpoints.background_change import (
    router as background_router,
)

main_router = APIRouter(prefix=f'/api/v{settings.api_version}')

main_router.include_router(
    background_router
)
