import logging

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.category import add_category, get_category_by_name, delete_category, get_category_by_id, \
    update_category
from apps.keyboards.default.admin import admin_category_keyboard
from apps.keyboards.inline.category import admin_category_detail_keyboard, CategoryDetail, admin_category_update_keyboard
from apps.states.admin import CategoryAdd, AdminMainMenu, CategoryUpdate
from loader import _
from apps.filters.is_admin import IsAdmin

router = Router()

@router.message(IsAdmin(),
                F.text.in_(["Categories 🍴", "Категории 🍴","Kategoriyalar 🍴"])
                )
async def admin_category_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession):
    await state.set_state(AdminMainMenu.category)
    text = "Category menu "
    await message.answer(text=text,
    reply_markup=await admin_category_keyboard(
        session=session,chat_id=message.chat.id
    ))

@router.message(IsAdmin(),AdminMainMenu.category , F.text.in_(["Add category 🍴"]))
async def add_category_handler(message: types.Message, state: FSMContext):
    text = "Enter name in uzbek"
    await message.answer(text=text,
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAdd.name_uz)

@router.message(IsAdmin(), CategoryAdd.name_uz)
async def add_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(name_uz=message.text)
    text = "Enter name in russian"
    await message.answer(text=text,
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAdd.name_ru)

@router.message(IsAdmin(), CategoryAdd.name_ru)
async def add_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(name_ru=message.text)
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
    await state.update_data(name_en=message.text)

    data = await state.get_data()
    if await add_category(session=session,data=data):
        text =_("Category is added")
    else:
        text = _("Something went wrong, please try again later")
    await message.answer(text=text,
                         reply_markup=await admin_category_keyboard(
                             session=session,chat_id=message.chat.id
                         ))
    await state.set_state(AdminMainMenu.category)


@router.callback_query(IsAdmin(), AdminMainMenu.category, CategoryDetail.filter(F.act=="delete_category"))
async def admin_category_detail_handler(
        call: CallbackQuery, session: AsyncSession,
        callback_data: CategoryDetail
):
    if await delete_category(
            session=session,
            category_id=callback_data.category_id
    ):
        text =_("Delete category id:")
        await call.answer(text=f"{text} {callback_data.category_id}",show_alert=True)
        await call.message.delete()
        text = "Category menu"
        await call.message.answer(
            text=text,
            reply_markup=await admin_category_keyboard(
                session=session, chat_id=call.message.chat.id
            ))
    else:
        await call.answer(text="Something went wrong ❌")

@router.callback_query(IsAdmin(),AdminMainMenu.category, CategoryDetail.filter(F.act=="update_category"))
async def admin_category_update_handler(
        callback: types.CallbackQuery,
        session: AsyncSession
):
    data = CategoryDetail.unpack(callback.data)
    category = await get_category_by_id(session=session, category_id=data.category_id)

    await callback.message.answer(text=_("Choose action:"),
                         reply_markup=await
                         admin_category_update_keyboard(
                             category=category
                             ))

@router.callback_query(IsAdmin(),AdminMainMenu.category, CategoryDetail.filter(F.act=="update_name"))
async def admin_category_update_handler(
        callback: types.CallbackQuery,
        session: AsyncSession,
        state: FSMContext
):
    data = CategoryDetail.unpack(callback.data)
    await state.update_data(category_id=data.category_id)

    await callback.message.answer(text=_("enter new category name in uzbek:"),reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryUpdate.name_uz)

@router.message(IsAdmin(), CategoryUpdate.name_uz)
async def admin_category_update_handler(message: types.Message, state: FSMContext):
    await state.update_data(name_uz=message.text)
    text = "Enter new name in russian:"
    await message.answer(text=text,reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryUpdate.name_ru)

@router.message(IsAdmin(), CategoryUpdate.name_ru)
async def admin_category_update_handler(message: types.Message, state: FSMContext):
    await state.update_data(name_ru=message.text)
    text = "Enter new name in english:"
    await message.answer(text=text,reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryUpdate.name_en)

@router.message(IsAdmin(), CategoryUpdate.name_en)
async def update_category_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(name_en=message.text)
    data = await state.get_data()
    category_id = data.get("category_id")
    if category_id is None:
        await message.answer("Error , category id has not found❌")
        return
    logging.info(f"Updating category ID: {category_id}")
    updated = await update_category(session=session, category_id=category_id, data=data)

    if updated:
        text =_("Category is updated✅")
    else:
        text = _("Something went wrong, please try again later❌")
    await message.answer(text=text,
                         reply_markup=await admin_category_keyboard(
                             session=session,chat_id=message.chat.id
                         ))




@router.message(IsAdmin(), AdminMainMenu.category)
async def accept_all_messages_category_handler(
            message: types.Message,
            session: AsyncSession
):

    category = await get_category_by_name(session=session, name=message.text)
    if category:
        text = f"""
Uzbek: {category.name['uz']}
Russian: {category.name['ru']}
English: {category.name['en']}
 """
        await message.answer(text=text,
                             reply_markup=await admin_category_detail_keyboard(
                            category=category
                        ))