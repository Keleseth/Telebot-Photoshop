from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from redis.asyncio import Redis

from bot.callbacks.whitelist_callbacks import WhiteListCallback
from bot.constants import (
    ADMIN_ZONE,
    ASK_ID_TO_ADD_BUTTON_TEXT,
    ASK_ID_TO_REMOVE_BUTTON_TEXT,
    ASK_ID_TO_SEARH_BUTTON_TEXT,
    FIND_USER_BUTTON_TEXT,
    WHITELIST_BUTTON_TEXT,
    REDIS_WHITELIST_KEY
)
from bot.states.whitelist_process import WhitelistState
from bot.keyboards.main_keyboards import admin_inline_kb


wl_handle_router = Router()


@wl_handle_router.message(F.text == ADMIN_ZONE)
async def open_admin_zone(message: Message):
    await message.answer('Админ-меню:', reply_markup=admin_inline_kb)


@wl_handle_router.callback_query(
    WhiteListCallback.filter(F.action == 'search')
)
async def cb_search_for_user(cb: CallbackQuery, state: FSMContext):
    await state.set_state(WhitelistState.waiting_for_id_to_search)
    await cb.message.edit_text(
        text=ASK_ID_TO_SEARH_BUTTON_TEXT,
        reply_markup=None
    )
    await cb.answer()


@wl_handle_router.callback_query(
    WhiteListCallback.filter(F.action == 'add')
)
async def cb_add_user(cb: CallbackQuery, state: FSMContext):
    await state.set_state(WhitelistState.waiting_for_id_to_add)
    await cb.message.edit_text(
        text=ASK_ID_TO_ADD_BUTTON_TEXT,
        reply_markup=None
    )
    await cb.answer()


@wl_handle_router.callback_query(
    WhiteListCallback.filter(F.action == 'remove')
)
async def cb_remove_user(cb: CallbackQuery, state: FSMContext):
    await state.set_state(WhitelistState.waiting_for_id_to_remove)
    await cb.message.edit_text(
        text=ASK_ID_TO_REMOVE_BUTTON_TEXT,
        reply_markup=None
    )
    await cb.answer()


@wl_handle_router.message(
    WhitelistState.waiting_for_id_to_search,
    F.text
)
async def search_user_in_wl(
    message: Message,
    state: FSMContext,
    redis: Redis
):
    uid = message.text.strip()
    if not uid.isdigit():
        await message.answer('ID должен быть числом. Попробуйте ещё раз.')
        return
    user_in_list = await redis.sismember(REDIS_WHITELIST_KEY, uid)
    text = (
        '✅ Пользователь найден в VIP списке' 
        if user_in_list 
        else '❌ Пользователь отсутствует в vip списке'
    )
    await message.answer(text=text)
    await state.clear()


@wl_handle_router.message(
    WhitelistState.waiting_for_id_to_add,
    F.text
)
async def add_user_to_wl(message: Message, state: FSMContext, redis: Redis):
    uid = message.text.strip()
    if not uid.isdigit():
        await message.answer('ID должен быть числом. Попробуйте ещё раз.')
        return
    added = await redis.sadd(REDIS_WHITELIST_KEY, uid)
    await message.answer(
        (
            '✅ Пользователь обавлен.'
            if added
            else 'Пользователь уже был в списке.'
        )
    )
    await state.clear()


@wl_handle_router.message(
    WhitelistState.waiting_for_id_to_remove,
    F.text
)
async def remove_user_from_wl(message: Message, state: FSMContext, redis: Redis):
    uid = message.text.strip()
    if not uid.isdigit():
        await message.answer('ID должен быть числом. Попробуйте ещё раз.')
        return
    removed = await redis.srem(REDIS_WHITELIST_KEY, uid)
    await message.answer(
        (
            'Пользователь Удалён из списка'
            if removed
            else 'Пользователя не было в списке.'
        )
    )
    await state.clear()



# @wl_handle_router.message()
# async def ask_user_id_for_search(message: Message, state: FSMContext):
#     await message.answer('Введите Telegram ID пользователя:')
#     await state.set_state(WhitelistState.waiting_for_id_to_search)


# @wl_handle_router.message(
#     WhiteListCallback(action='search'), WhitelistState.waiting_for_id_to_search
# )
# async def process_user_search_in_wl(
#     callback: CallbackQuery,
#     redis: Redis,
#     state: FSMContext
# ):
#     user_id = callback.message.text.strip()
#     user_in_wl = await redis.sismember(REDIS_WHITELIST_KEY, user_id)
#     if user_in_wl:
#         await message.answer(
#             text=f"✅ Пользователь: {user_id} есть в vip списке"
#         )
#     else:
#         await message.answer(
#             f'❌ Пользователь {user_id} не найден в vip списке'
#         )
#     await state.clear()


# @wl_handle_router.message(
#     F.text.isdigit(), WhitelistState.waiting_for_id_to_search
# )
# async def process_user_search_in_wl(
#     message: Message,
#     redis: Redis,
#     state: FSMContext
# ):
#     user_id = message.text.strip()
#     user_in_wl = await redis.sismember(REDIS_WHITELIST_KEY, user_id)
#     if user_in_wl:
#         await message.answer(
#             text=f"✅ Пользователь: {user_id} есть в vip списке"
#         )
#     else:
#         await message.answer(
#             f'❌ Пользователь {user_id} не найден в vip списке'
#         )
#     await state.clear()


