import os
from redis.asyncio.client import Redis

from bot.constants import (
    REDIS_ADMINS_KEY,
    REDIS_WHITELIST_KEY
)


async def init_admin(redis: Redis):
    admin_id = os.getenv('BOT_FIRST_ADMIN')
    if admin_id:
        await redis.sadd(REDIS_ADMINS_KEY, admin_id)


async def is_admin(redis: Redis, user_id: int) -> bool:
    return await redis.sismember(REDIS_ADMINS_KEY, str(user_id))


async def add_to_whitelist(redis: Redis, user_id: int):
    await redis.sadd(REDIS_WHITELIST_KEY, str(user_id))


async def remove_from_whitelist(redis: Redis, user_id: int):
    await redis.srem(REDIS_WHITELIST_KEY, str(user_id))


async def is_whitelisted(redis: Redis, user_id: int) -> bool:
    return await redis.sismember(REDIS_WHITELIST_KEY, str(user_id))