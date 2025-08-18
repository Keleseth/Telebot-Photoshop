from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.photo_callbacks import PhotoActionCallback


def kb_photo_options():

    builder = InlineKeyboardBuilder()
    builder.button(
        text='Убрать фон',
        callback_data=PhotoActionCallback(
            action='rm_bg'
        ).pack()
    )
    builder.adjust(1)
    return builder.as_markup()