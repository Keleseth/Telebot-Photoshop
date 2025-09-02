from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.callbacks.whitelist_callbacks import WhiteListCallback
from bot.constants import (
    ADD_USER_BUTTON_TEXT,
    ADMIN_ZONE,
    CANCEL_BUTTON,
    FIND_USER_BUTTON_TEXT,
    REMOVE_USER_BUTTON_TEXT
)


def main_kb(is_admin: bool = False) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=CANCEL_BUTTON))
    if is_admin:
        kb.row(KeyboardButton(text=ADMIN_ZONE))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)


admin_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text=FIND_USER_BUTTON_TEXT,
            callback_data=WhiteListCallback(action='search').pack()
        ),
        InlineKeyboardButton(
            text=ADD_USER_BUTTON_TEXT,
            callback_data=WhiteListCallback(action='add').pack()
        ),
        InlineKeyboardButton(
            text=REMOVE_USER_BUTTON_TEXT,
            callback_data=WhiteListCallback(action='remove').pack()
        ),
    ]]
)
