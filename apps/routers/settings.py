from aiogram import types
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.location import get_location_, update_user_location
from apps.db_queries.user import update_user_language, get_language
from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.user import languages, location_share_keyboard

from apps.states.user import LocationState
from loader import _
from apps.keyboards.default.admin import user_settings_keyboard, admin_main_menu_keyboard
from apps.keyboards.default.user import user_main_keyboard
router = Router()


@router.message(F.text.in_(["Settings ⚙️","Настройки ⚙️","Sozlamalar ⚙️"]))
async def send_settings(message: types.Message, state: FSMContext):
    text = _("choose the action")
    await message.answer(text=text,reply_markup=await user_settings_keyboard())

@router.message(F.text.in_("Change language ✍️"))
async def change_language(message: types.Message, state: FSMContext):
    text = _("choose the language")
    await message.answer(text=text,reply_markup=languages)

@router.message(IsAdmin() ,F.text.in_(["Uzbek 🇺🇿", "Russian 🇷🇺", "English 🇺🇸"]))
async def set_language_admin(message: types.Message, state: FSMContext, session: AsyncSession):
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
async def set_language_user(message: types.Message, state: FSMContext, session: AsyncSession):
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

@router.message(F.text.in_(["see recent location 📍"]))
async def view_location(message: types.Message, session: AsyncSession):
    data = await get_location_(chat_id=message.from_user.id, session=session)
    if not data:
        await message.answer(text="you had not send any locations yet", reply_markup=await user_main_keyboard())
        return
    await message.answer_location(latitude=data["latitude"], longitude=data["longitude"], reply_markup=await user_main_keyboard())

@router.message(F.text.in_(["Change location 📝"]))
async def change_location(message: types.Message, session: AsyncSession, state:FSMContext):
    language = await get_language(message.from_user.id, session)

    await message.answer(
        _("please, share your location", locale=language),
        reply_markup=await location_share_keyboard(locale=language)
    )
    await state.set_state(LocationState.location)

@router.message(F.location ,StateFilter(LocationState.location))
async def save_location(message: types.Message, state: FSMContext, session: AsyncSession):
    try:
        lat = message.location.latitude
        lon = message.location.longitude


        language = await get_language(message.from_user.id, session)
        text = _("New location successfully added📍", locale=language)
        await update_user_location(chat_id=message.from_user.id, latitude=lat, longitude=lon, session=session)
        await message.answer(text=text, reply_markup=await user_main_keyboard(locale=language))
        await state.clear()
    except Exception as e:
        print(e)
