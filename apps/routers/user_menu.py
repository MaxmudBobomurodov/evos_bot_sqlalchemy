from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from apps.keyboards.inline.user import user_product_menu_inline_keyboard
from loader import _
from apps.keyboards.default.user import user_location_keyboard, user_product_menu

router = Router()

@router.message(F.text.in_(["Menu🍴"]))
async def on_menu(message: Message, session: AsyncSession):
    text = _("Now you can choose :")
    keyboard = await user_product_menu(session=session)
    if keyboard:
        await message.answer(text=text, reply_markup=await user_product_menu_inline_keyboard(session=session, chat_id=message.chat.id))
    else:
        await message.answer(text=_("No products available."))

