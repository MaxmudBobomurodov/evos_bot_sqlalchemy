from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.user import get_user
from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.admin import admin_main_menu_keyboard
from apps.keyboards.default.user import user_main_keyboard
from apps.keyboards.inline.user import languages
from apps.states.user import RegisterState
from loader import _

router = Router()

# @router.message()
# async def get_channel_id(message: types.Message):
#     if message.forward_from_chat:
#         await message.answer(f"Channel name: {message.forward_from_chat.title}\nID: {message.forward_from_chat.id}")
#     else:
#         await message.answer("this message is not forward from channel")


@router.message(Command('start'), IsAdmin())
async def admin_start_handler(message: types.Message):
    text = _("Assalomu alaykum, admin 🫡")
    await message.answer(text=text, reply_markup=await admin_main_menu_keyboard())


@router.message(Command('start'))
async def user_start_handler(message: types.Message, state: FSMContext, session: AsyncSession):
    user = await get_user(chat_id=message.chat.id, session=session)
    if not user:
        text = "Assalomu alaykum, please select the language !"
        await message.answer(text=text, reply_markup=languages)
        await state.set_state(RegisterState.language)
    else:
        text = _("Assalomu alaykum, welcome back")
        await message.answer(text=text, reply_markup=await user_main_keyboard())
