from aiogram.filters.callback_data import CallbackData


class PhotoActionCallback(CallbackData, prefix='photo'):

    action: str
