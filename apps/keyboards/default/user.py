from aiogram.types import KeyboardButton , ReplyKeyboardMarkup


user_phone_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="share phone number ☎️", request_contact=True)
    ]
], resize_keyboard=True, one_time_keyboard=True
)


user_main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="🍴 Menyu")
    ]
    ,
    [
        KeyboardButton(text="📋 Mening buyurtmalarim")
    ],
    [
        KeyboardButton(text="📥 Savat"),
        KeyboardButton(text="for 📞 Aloqa")
    ],
    [
        KeyboardButton(text="Send feedback ✍️"),
        KeyboardButton(text="settings")
    ]

],
resize_keyboard=True,
is_persistent=True
)

user_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Setlar")
    ],
    [
        KeyboardButton(text="Lavash"),
        KeyboardButton(text="burger")
    ],
    [
        KeyboardButton(text="🔙 Orqaga qaytish")
    ]
],
    resize_keyboard=True,
    is_persistent=True)

location_share = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Share location 🌏", request_location=True)
    ]], resize_keyboard=True, one_time_keyboard=True
)