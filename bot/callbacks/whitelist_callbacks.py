from aiogram.filters.callback_data import CallbackData


class WhiteListCallback(CallbackData, prefix='wl'):
    action: str

