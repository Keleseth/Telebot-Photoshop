from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(F.photo)
async def get_photo(
    message: Message,
    state: FSMContext
):
    await message.answer_photo(
        photo=message.photo[-1].file_id,
        caption='Лови фото обратно!'
    )
