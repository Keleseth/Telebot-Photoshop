from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.config import config
from bot.lexicon import ru, en


LANGUAGES = {
    'ru': ru.LEXICON_RU,
    'en': en.LEXICON_EN,
}

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    # TODO добавить в будущем проверку выбранного языка
    lang = config.default_lang
    lexicon = LANGUAGES.get(lang, LANGUAGES['ru'])
    await message.answer(
        text=lexicon['start']
    )
