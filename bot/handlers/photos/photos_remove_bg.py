import os
import aiohttp
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender


from bot.callbacks.photo_callbacks import PhotoActionCallback
from bot.states.photo_process import PhotoProcessState

API_BASE_URL = os.getenv('API_BASE_URL', 'http://api:8000')

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
    data = await state.get_data()
    file_id = data.get('last_photo_id')
    if not file_id:
        await callback.answer("Нет фото — пришли заново", show_alert=True)
        return

    await callback.message.edit_text('Опция выбрана: убрать фон', reply_markup=None)
    await callback.answer()
    await state.clear()

    async with ChatActionSender.upload_photo(bot=callback.bot, chat_id=callback.message.chat.id):
        tg_file = await callback.bot.get_file(file_id)
        file_bytes_io = await callback.bot.download_file(tg_file.file_path)
        img_bytes = file_bytes_io.getvalue()

        form = aiohttp.FormData()
        form.add_field(
            name='file',
            value=img_bytes,
            filename='input.jpg',
            content_type='image/jpeg',
        )
        timeout = aiohttp.ClientTimeout(total=120)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(f'{API_BASE_URL}/bg/remove', data=form) as resp:
                body = await resp.read()
                if resp.status != 200 or not body:
                    await callback.message.answer(f'API {resp.status}: {body[:200]!r}')
                    return
        img = BufferedInputFile(body, filename="no-bg.png")
        await callback.message.answer_photo(photo=img, caption="Готово 🎯 фон убран")
