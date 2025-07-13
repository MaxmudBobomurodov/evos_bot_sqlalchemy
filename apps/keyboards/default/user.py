from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from loader import _
async def user_phone_keyboard(locale=None):
    return ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=_("share phone number ☎️", locale=locale), request_contact=True)
    ]
], resize_keyboard=True, one_time_keyboard=True
)

async def user_main_keyboard(locale=None):
    return ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=_("Menu🍴", locale=locale))
    ]
    ,
    [
        KeyboardButton(text=_("My Orders📋", locale=locale))
    ],
    [
        KeyboardButton(text=_("Send feedback ✍️"),locale=locale),
        KeyboardButton(text=_("Settings ⚙️"),locale=locale)
    ]

    ],
    resize_keyboard=True,
    is_persistent=True
    )

async def user_location_keyboard(locale=None):
    return ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=_("My address 📍"),locale=locale),
        KeyboardButton(text=_("Send address 📝"), locale=locale)
    ],
    [
        KeyboardButton(text=_("Back ⬅️"),locale=locale)
    ]
    ],
        resize_keyboard=True,
        is_persistent=True)


async def location_share_keyboard(locale=None):
    return ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text=_("Share location 🌏",locale=locale), request_location=True)
    ]], resize_keyboard=True, one_time_keyboard=True
    )

languages = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Uzbek 🇺🇿"),
        KeyboardButton(text="Russian 🇷🇺"),
        KeyboardButton(text="English 🇺🇸"),
    ]],
    resize_keyboard=True,
    is_persistent=True
)

async def user_product_menu(session: AsyncSession):
    stmt = select(Product).order_by(Product.id)
    result = await session.execute(stmt)
    products = result.scalars().all()

    if not products:
        return None

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{product.name} — {product.price} so'm",
                callback_data=f"product:{product.id}"
            )]
            for product in products
        ]
    )
    return keyboard