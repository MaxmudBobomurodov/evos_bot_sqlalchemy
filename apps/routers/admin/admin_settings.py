from aiogram import types
from aiogram import Router, F


from sqlalchemy.ext.asyncio import AsyncSession
from apps.db_queries.user import update_user_language
from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.user import languages

from loader import _
from apps.keyboards.default.admin import admin_main_menu_keyboard, admin_settings_keyboard
from apps.keyboards.default.user import user_main_keyboard

router =Router()


@router.message(IsAdmin(),F.text.in_(["Settings ⚙️","Настройки ⚙️","Sozlamalar ⚙️"]))
async def send_settings(message: types.Message):
    text = _("choose the action")
    await message.answer(text=text,reply_markup=await admin_settings_keyboard())

@router.message(IsAdmin(),F.text.in_("Change language ✍️"))
async def change_language(message: types.Message):
    text = _("choose the language")
    await message.answer(text=text,reply_markup=languages)

@router.message(IsAdmin() ,F.text.in_(["Uzbek 🇺🇿", "Russian 🇷🇺", "English 🇺🇸"]))
async def set_language_admin(message: types.Message, session: AsyncSession):
    lang_map = {
        "Uzbek 🇺🇿": "uz",
        "Russian 🇷🇺": "ru",
        "English 🇺🇸": "en"
    }

    selected_lang = lang_map.get(message.text)
    if selected_lang:
        await update_user_language(user_id=message.from_user.id, language=selected_lang, session=session)
        text = _("Language has been updated ✅", locale=selected_lang)
        await message.answer(text=text, reply_markup=await admin_main_menu_keyboard())

@router.message(F.text.in_(["Uzbek 🇺🇿", "Russian 🇷🇺", "English 🇺🇸"]))
async def set_language_user(message: types.Message,session: AsyncSession):
    lang_map = {
        "Uzbek 🇺🇿": "uz",
        "Russian 🇷🇺": "ru",
        "English 🇺🇸": "en"
    }

    selected_lang = lang_map.get(message.text)
    if selected_lang:
        await update_user_language(user_id=message.from_user.id, language=selected_lang, session=session)
        text = _("Language has been updated ✅", locale=selected_lang)
        await message.answer(text=text, reply_markup=await user_main_keyboard())