from aiogram import Router
from aiogram.filters import BaseFilter


def attach_filter_to_router(router: Router, filter_: BaseFilter) -> Router:
    router.message.filter(filter_)
    router.callback_query.filter(filter_)
    return router
