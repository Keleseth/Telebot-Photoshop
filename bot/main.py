import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from redis.asyncio import Redis

from bot.config import config
from bot.constants import (
    REDIS_ADMINS_KEY,
    REDIS_WHITELIST_KEY
)
from bot.filters.is_admin import IsAdminFilter
from bot.handlers import (
    bg_color_change_router,
    incoming_photos_router,
    rm_bg_router,
    start_router,
    wl_handle_router
)
from bot.middlewares import (
    IsAdminMiddleware,
    ProvideRedisMiddlware,
    RedisThrottlingMiddleware,
)
from bot.services.redis_admin import init_admin
from bot.services.filters import attach_filter_to_router


async def main():
    # Логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Сессия бота с таймаутами для безопасности
    session = AiohttpSession(
        timeout=30  # таймаут на запросы к Telegram API
    )

    bot = Bot(
        token=config.bot_token.get_secret_value(),
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    # FSM-хранилище (память — для начала, потом Redis)
    storage = MemoryStorage()
    redis = Redis(
        host=config.redis_host,
        port=config.redis_port,
        decode_responses=True
    )
    await init_admin(redis)
    bg_color_change_router.message.middleware(
        RedisThrottlingMiddleware(
            redis=redis,
            redis_filter_keys=[REDIS_ADMINS_KEY, REDIS_WHITELIST_KEY]
        ),
    )

    dp = Dispatcher(storage=storage)
    start_router.message.middleware(IsAdminMiddleware(redis=redis))
    dp.include_router(start_router)
    attach_filter_to_router(wl_handle_router, IsAdminFilter(redis=redis))
    wl_handle_router.message.middleware(ProvideRedisMiddlware(redis))
    wl_handle_router.callback_query.middleware(ProvideRedisMiddlware(redis))
    dp.include_router(wl_handle_router)
    dp.include_router(incoming_photos_router)
    dp.include_router(bg_color_change_router)
    dp.include_router(rm_bg_router)

    # Регистрируем все хэндлеры из пакета handlers
    # register_all_handlers(dp) #TODO написать функцию массовой регистрации

    try:
        logging.info('🚀 Бот запущен')
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types()
        )
    except Exception as e:
        logging.exception(f'Ошибка в работе бота: {e}')
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
