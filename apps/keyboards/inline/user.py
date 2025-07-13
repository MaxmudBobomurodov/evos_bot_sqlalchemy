from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.product import get_product
from apps.db_queries.user import get_user
from core.models import Product

languages = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Uzbek 🇺🇿", callback_data="uz"),
        InlineKeyboardButton(text="Russian 🇷🇺", callback_data="ru"),
        InlineKeyboardButton(text="English 🇺🇸", callback_data="en"),
    ]]
)
async def user_product_menu_inline_keyboard(session: AsyncSession, chat_id: int):
    user = await get_user(session=session, chat_id=chat_id)
    lang = user.language or "en"

    products: Sequence[Product] = await get_product(session=session) or []
    keyboard = []
    row = []
    for product in products:
        name = product.name.get(lang, product.name.get("en", "Unnamed"))
        text = f"{name} — {product.price} so'm"
        row.append(InlineKeyboardButton(text=text, callback_data=str(product.id)))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )