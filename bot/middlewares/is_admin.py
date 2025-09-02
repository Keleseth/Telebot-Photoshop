from aiogram import BaseMiddleware
from redis.asyncio import Redis

from bot.constants import REDIS_ADMINS_KEY


class IsAdminMiddleware(BaseMiddleware):

    def __init__(self, redis: Redis):
        self.redis = redis


    async def __call__(
        self, handler, event, data
    ):
        is_admin = False
        if getattr(event, 'from_user', None):
            user_id = str(event.from_user.id)
            is_admin = await self.redis.sismember(REDIS_ADMINS_KEY, user_id)
        
        data['is_admin'] = bool(is_admin)
        return await handler(event, data)
