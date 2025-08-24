from fastapi import FastAPI
import os
from redis.asyncio import Redis

from app.config import settings
from app.api.v1.router import main_router

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    version='1.0.0'
)
app.include_router(main_router)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = Redis.from_url(REDIS_URL, decode_responses=True)

@app.get("/health")
async def health():
    ok = await r.ping()
    return {"status": "ok", "redis": ok}
