from fastapi import APIRouter

from app.api.v1.endpoints.background_change import (
    router as background_router
)


main_router = APIRouter()
main_router.include_router(background_router)