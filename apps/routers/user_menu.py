from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from loader import _
from apps.keyboards.default.user import user_location_keyboard

router = Router()

@router.message(F.text.in_([""]))
async def on_menu(message: Message, session: AsyncSession):
    text = _("choose action:")
    await message.answer(text=text, reply_markup=await user_location_keyboard())