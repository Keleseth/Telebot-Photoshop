from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.config import config
from bot.keyboards.main_keyboards import main_kb
from bot.lexicon import ru, en
from bot.constants import CANCEL_BUTTON


LANGUAGES = {
    'ru': ru.LEXICON_RU,
    'en': en.LEXICON_EN,
}

router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    is_admin: bool = False
):
    # TODO добавить в будущем проверку выбранного языка
    lang = config.default_lang
    lexicon = LANGUAGES.get(lang, LANGUAGES['ru'])
    # reply_kb = admin_kb if is_admin else ReplyKeyboardRemove()
    await message.answer(
        text=lexicon['start'],
        reply_markup=main_kb(is_admin=is_admin)
    )


@router.message(F.text.in_({CANCEL_BUTTON, '/cancel'}))
async def reset_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выбранное действие отменено.')
