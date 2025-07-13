from aiogram.types import KeyboardButton , ReplyKeyboardMarkup
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
