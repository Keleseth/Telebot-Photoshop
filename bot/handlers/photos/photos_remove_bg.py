import aiohttp, json, os
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    ContentType,
    Message,
    ReplyKeyboardRemove
)
from aiogram.utils.chat_action import ChatActionSender
from redis.asyncio import Redis

from bot.callbacks.photo_callbacks import (
    PhotoActionCallback
)
from bot.constants import (
    CHOOSE_COLOR,
    CHOSEN_OPTION_RM_BG,
    INCORRECT_COLOR,
    NETIFY_PALLETE_URL,
    NO_COLOR,
    NO_PHOTO,
    SERVER_ERROR,
)
from bot.keyboards.photo_keyaboards import kb_palette
from bot.states.photo_process import PhotoProcessState


API_BASE_URL = os.getenv('API_BASE_URL', 'http://api:8000/api/v1')

rm_bg_router = Router(name='photo_remove_bg')
bg_color_change_router = Router(name='bg_color_change')

@rm_bg_router.callback_query(
    PhotoActionCallback.filter(F.action == 'rm_bg'),
    PhotoProcessState.waiting_instructions
)
async def photo_remove_bg_option(
    callback: CallbackQuery,
    callback_data: PhotoActionCallback,
    state: FSMContext
):
    data = await state.get_data()
    file_id = data.get('last_photo_id')
    if not file_id:
        await callback.answer(NO_PHOTO, show_alert=True)
        return
    await callback.message.edit_text(CHOSEN_OPTION_RM_BG, reply_markup=None)
    # await callback.message.answer(
    #     text='Откройте палитру, выберите цвет и подтвердите.',
    #     reply_markup=kb_palette()
    # )
    await callback.message.answer(
        text=CHOOSE_COLOR,
        reply_markup=kb_palette(NETIFY_PALLETE_URL)
    )
    await state.update_data(file_id=file_id)
    await state.set_state(PhotoProcessState.waiting_bg_color)


@bg_color_change_router.message(
    F.content_type == ContentType.WEB_APP_DATA,
    PhotoProcessState.waiting_bg_color,
)
async def color_selected_from_webapp(
    message: Message,
    state: FSMContext
):
    try:
        data = await state.get_data()
        file_id = data.get('last_photo_id')
        payload = json.loads(message.web_app_data.data)
        chosen_hex_color = payload.get('hex')
        if not chosen_hex_color:
            await message.answer(NO_COLOR)
            return
        await state.update_data(bg_color_hex=chosen_hex_color)

        async with ChatActionSender.upload_photo(
            bot=message.bot,
            chat_id=message.chat.id
        ):
            image_metadata = await message.bot.get_file(file_id=file_id)
            image_bytes_io = await message.bot.download_file(
                file_path=image_metadata.file_path
            )
            image_bytes = image_bytes_io.getvalue()
            form = aiohttp.FormData()
            form.add_field(
                name='image',
                value=image_bytes,
                filename='input.jpg',
                content_type='image/jpeg'
            )
            form.add_field(
                name='color',
                value=chosen_hex_color,
            )
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f'{API_BASE_URL}/bg/remove',
                    data=form
                ) as resp:
                    body = await resp.read()
                    if resp.status != 200 or not body:
                        await message.answer(
                            SERVER_ERROR,
                            reply_markup=ReplyKeyboardRemove()
                        )
                        await state.clear()
                        return
            new_image = BufferedInputFile(body, filename='updated_photo.png')
            await message.answer_photo(
                photo=new_image,
                caption='Готово 🎯',
                reply_markup=ReplyKeyboardRemove()
            )
            await state.clear()

    except Exception as e:
        await message.answer(
            INCORRECT_COLOR,
        )
        raise e
