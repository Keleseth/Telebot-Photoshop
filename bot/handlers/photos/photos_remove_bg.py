from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.photo_callbacks import PhotoActionCallback
from bot.states.photo_process import PhotoProcessState


router = Router(name='photo_remove_bg')

@router.callback_query(
    PhotoActionCallback.filter(F.action == 'rm_bg'),
    PhotoProcessState.waiting_instructions
)
async def photo_remove_bg(
    callback: CallbackQuery,
    callback_data: PhotoActionCallback,
    state: FSMContext
):
    print('сюда пришло --------------')
    data = await state.get_data()
    file_id = data.get('last_photo_id')
    if not file_id:
        await callback.answer("Нет фото — пришли заново", show_alert=True)
        return
    await callback.message.edit_text(
        'Опция выбрана: убрать фон',
        reply_markup=None
    )
    await callback.answer()
    await state.clear()
