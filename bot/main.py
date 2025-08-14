import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from bot.config import config
from bot.handlers import (
    start,
    photos
)


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
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    # FSM-хранилище (память — для начала, потом Redis)
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.include_router(start.router)
    dp.include_router(photos.router)

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
