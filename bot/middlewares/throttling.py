from typing import Sequence

from aiogram import BaseMiddleware
from aiogram.types import Message, ReplyKeyboardRemove
from typing import Callable, Dict, Any, Awaitable
from redis.asyncio import Redis
from datetime import datetime

from bot.config import config
from bot.constants import LIMIT_EXCEEDED


class RedisThrottlingMiddleware(BaseMiddleware):
    """
    Middleware that limits the number of allowed actions (e.g. photo uploads)
    per user per day, using Redis as a counter.

    - Skips throttling for users present in the specified Redis sets
      (e.g. ***, ***) contained in redis_filter_keys.
    - For all other users, increments a daily counter in Redis under
      the key pattern: "photo_limit:{user_id}:{YYYY-MM-DD}".
    - If the counter exceeds `config.photo_limit_per_day`, the event
      is blocked and a warning message is sent.
    - The counter automatically expires after a set number of hours.

    Args:
        redis (Redis): Active Redis connection.
        redis_filter_keys (Sequence[str]): Redis set keys that contain
            user IDs which should bypass throttling.
    """
    def __init__(
        self, 
        redis: Redis,
        redis_filter_keys: Sequence[str]
    ):
        self.redis = redis
        self.redis_filter_keys = redis_filter_keys

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not getattr(event, "from_user", None):
            return await handler(event, data)

        user_id = str(event.from_user.id)
        for key in self.redis_filter_keys:
            if await self.redis.sismember(key, user_id):
                return await handler(event, data)

        today_key = f"photo_limit:{user_id}:{datetime.utcnow().date()}"
        count = await self.redis.get(today_key)

        if count is not None and int(count) >= config.photo_limit_per_day:
            await event.answer(
                LIMIT_EXCEEDED,
                reply_markup=ReplyKeyboardRemove()
            )
            state = data.get('state')
            if state:
                await state.clear()
            return

        try:
            result = await handler(event, data)
        except Exception as e:
            raise
        else:
            await self.redis.incr(today_key)
            await self.redis.expire(today_key, 86400)

        return result
