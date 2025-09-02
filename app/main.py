from fastapi import FastAPI

from app.config import settings
from app.api.v1.router import main_router

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    version=settings.api_version
)
app.include_router(main_router)
