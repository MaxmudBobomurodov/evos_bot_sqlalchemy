from typing import Sequence

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.category import get_categories
from apps.db_queries.product import get_product
from apps.db_queries.user import get_user
from core.models import Category, Product
from loader import _

async def admin_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Products 🍴")),
                KeyboardButton(text=_("Categories 🍴"))
            ],
            [
                KeyboardButton(text=_("Users 👯")),
                KeyboardButton(text=_("Orders 📝"))
            ],
            [
                KeyboardButton(text=_("Settings ⚙️"))
            ]
        ], resize_keyboard=True
    )

async def admin_category_keyboard(session: AsyncSession, chat_id: int):
    user = await get_user(session=session, chat_id=chat_id)
    lang = user.language or "en"

    categories: Sequence[Category] = await get_categories(session=session)
    keyboard = [
        [
            KeyboardButton(text=_("Add category 🍴")),
            KeyboardButton(text=_("Back ⬅️"))
        ]
    ]
    row = []
    for category in categories:
        name = category.name.get(lang, category.name.get("en", "Unnamed"))
        row.append(KeyboardButton(text=name))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
async def admin_product_keyboard(session: AsyncSession, chat_id: int):
    user = await get_user(session=session, chat_id=chat_id)
    lang = user.language or "en"

    products: Sequence[Product] = await get_product(session=session) or []
    keyboard = [
        [
            KeyboardButton(text=_("Add product🍴")),
            KeyboardButton(text=_("Back ⬅️"))
        ]
    ]
    row = []
    for product in products:
        name = product.name.get(lang, product.name.get("en", "Unnamed"))
        row.append(KeyboardButton(text=name))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

async def user_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Change language ✍️")),
                KeyboardButton(text=_("Back ⬅️"))
            ],
            [
                KeyboardButton(text=_("Change location 📝")),
                KeyboardButton(text=_("see recent location 📍"))
            ]
        ], resize_keyboard=True
    )
