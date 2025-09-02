from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    WebAppInfo
)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from bot.callbacks.photo_callbacks import (
    BackgroundCallback,
    PhotoActionCallback,
)
from bot.constants import BG_COLOR_CHOICES, NETIFY_PALLETE_URL


def kb_photo_options() -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.button(
        text='Убрать фон',
        callback_data=PhotoActionCallback(
            action='rm_bg'
        ).pack()
    )
    builder.adjust(1)
    return builder.as_markup()


def kb_background_colors() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for title, value in BG_COLOR_CHOICES:
        builder.button(
            text=title,
            callback_data=BackgroundCallback(color=value)
        )
    builder.adjust(1)
    return builder.as_markup()


def kb_palette():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🎨 Выбрать палитру",
        web_app=WebAppInfo(url=NETIFY_PALLETE_URL)
    )
    builder.adjust(1)
    return builder.as_markup()


def kb_palette(url: str):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(
            text="🌈 Выбрать цвет (WebApp)",
            web_app=WebAppInfo(url=NETIFY_PALLETE_URL)
        )]],
        resize_keyboard=True
    )


# def kb_palette_inline(url: str) -> InlineKeyboardMarkup:
#     kb = InlineKeyboardBuilder()
#     kb.button(
#         text='🌈 Выбрать цвет (WebApp)',
#         web_app=WebAppInfo(url=url)  # ВАЖНО: web_app, не url
#     )
#     kb.adjust(1)
#     return kb.as_markup()
