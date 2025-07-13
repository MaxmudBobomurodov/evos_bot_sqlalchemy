from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession
from loader import _
from apps.keyboards.default.user import user_location_keyboard, user_product_menu

router = Router()

@router.message(F.text.in_(["Menu🍴"]))
async def on_menu(message: Message, session: AsyncSession):
    text = _("Now you can choose :")
    keyboard = await user_product_menu(session=session)
    if keyboard:
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text=_("No products available."))
