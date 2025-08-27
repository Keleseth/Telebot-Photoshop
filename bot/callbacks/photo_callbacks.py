from aiogram.filters.callback_data import CallbackData


class PhotoActionCallback(CallbackData, prefix='photo'):
    """
    CallbackData для всех вариантов работы с фото.
    """

    action: str


class BackgroundCallback(CallbackData, prefix='background'):
    """
    CallbackData для всех вариантов работы с фото.
    """

    color: str
