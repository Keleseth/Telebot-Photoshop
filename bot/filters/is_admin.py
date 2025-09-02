from aiogram.filters import BaseFilter
from aiogram.types import Message
from redis.asyncio import Redis

from bot.constants import REDIS_ADMINS_KEY


class IsAdminFilter(BaseFilter):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def __call__(self, message: Message) -> bool:
        return await self.redis.sismember(
            REDIS_ADMINS_KEY, str(message.from_user.id)
        )
