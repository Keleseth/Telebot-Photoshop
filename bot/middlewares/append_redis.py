from aiogram import BaseMiddleware

from redis.asyncio import Redis


class ProvideRedisMiddlware(BaseMiddleware):

    def __init__(self, redis: Redis):
        self.redis = redis


    async def __call__(self, handler, event, data):
        data['redis'] = self.redis
        return await handler(event, data)
