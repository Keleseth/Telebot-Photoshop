from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.callbacks.photo_callbacks import PhotoActionCallback
from bot.keyboards.photo_keyaboards import kb_photo_options
from bot.states.photo_process import PhotoProcessState


router = Router()


@router.message(
    F.photo,
    StateFilter(None)
)
async def get_photo(
    message: Message,
    state: FSMContext
):
    await state.update_data(last_photo_id=message.photo[-1].file_id)
    await message.answer(
        text='Выбери опциию из списка',
        reply_markup=kb_photo_options()
    )
    await state.set_state(PhotoProcessState.waiting_instructions)
