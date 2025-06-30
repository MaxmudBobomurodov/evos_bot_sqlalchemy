from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.category import add_category
from apps.keyboards.default.admin import admin_category_keyboard
from apps.states.admin import CategoryAdd
from loader import _
from apps.filters.is_admin import IsAdmin

router = Router()

@router.message(IsAdmin(), F.text.in_(["Categories 🍴", "Категории 🍴","Kategoriyalar 🍴"]))
async def admin_category_handler(message: types.Message, session: AsyncSession):
    text = "Category menu "
    await message.answer(text=text,
    reply_markup=await admin_category_keyboard(
        session=session,chat_id=message.chat.id
    ))

@router.message(IsAdmin(), F.text.in_(["Add category 🍴"]))
async def add_category_handler(message: types.Message, state: FSMContext):
    text = "Enter name in uzbek"
    await message.answer(text=text,
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAdd.name_uz)

@router.message(IsAdmin(), CategoryAdd.name_uz)
async def add_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(uz=message.text)
    text = "Enter name in russian"
    await message.answer(text=text,
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAdd.name_ru)

@router.message(IsAdmin(), CategoryAdd.name_ru)
async def add_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(ru=message.text)
    text = "Enter name in english"
    await message.answer(text=text,
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAdd.name_en)

@router.message(IsAdmin(), CategoryAdd.name_en)
async def add_category_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(en=message.text)

    data = await state.get_data()
    if await add_category(session=session,data=data):
        text =_("Category is added")
    else:
        text = _("Something went wrong, please try again later")
    await message.answer(text=text,
                         reply_markup=await admin_category_keyboard(
                             session=session,chat_id=message.chat.id
                         ))
    await state.clear()