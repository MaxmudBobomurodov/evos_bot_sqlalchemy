from ast import increment_lineno

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.product import add_product
from apps.keyboards.default.admin import admin_product_keyboard
from apps.filters.is_admin import IsAdmin
from apps.keyboards.inline.category import admin_category_inline_keyboard
from apps.states.admin import ProductAdd, AdminMainMenu

router = Router()
@router.message(IsAdmin(), F.text.in_(["Products 🍴","Продукция 🍴","Mahsulotlar 🍴"]))
async def admin_category_handler(message: types.Message,
                                 session: AsyncSession,
                                 state: FSMContext):
    text = "product menu "
    await message.answer(text=text,
    reply_markup=await admin_product_keyboard(session=session, chat_id=message.chat.id))
    await state.set_state(AdminMainMenu.product)


@router.message(IsAdmin(),AdminMainMenu.product,F.text.in_(["Add product🍴","Mahsulot qo'shish🍴","Добавить продукт🍴"]))
async def get_category_id(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession):
    text = "Please select category:"
    await message.answer(text=text, reply_markup=await admin_category_inline_keyboard(
        session=session,
        chat_id=message.chat.id))
    await state.set_state(ProductAdd.category)


@router.callback_query(IsAdmin(), ProductAdd.category)
async def add_category_handler(call: CallbackQuery,
                           state: FSMContext):
    try:
        category_id = int(call.data)
        await state.update_data(category_id=category_id)
    except ValueError:
        await call.message.answer("Please , enter right category id❌ .")
        return
    text = "Enter product name in uzbek"
    await call.message.answer(text=text,
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.name_uz)

@router.message(IsAdmin(), ProductAdd.name_uz)
async def add_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(name_uz=message.text)
    text = "Enter product name in russian"
    await message.answer(text=text,
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.name_ru)

@router.message(IsAdmin(), ProductAdd.name_ru)
async def add_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(name_ru=message.text)
    text = "Enter product name in english"
    await message.answer(text=text,
    reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.name_en)

@router.message(IsAdmin(),ProductAdd.name_en)
async def get_name_en(message: types.Message, state: FSMContext):
    await state.update_data(name_en=message.text)
    await message.answer("Enter product description in Uzbek:")
    await state.set_state(ProductAdd.about_uz)

@router.message(IsAdmin(),ProductAdd.about_uz)
async def get_about_uz(message: types.Message, state: FSMContext):
    await state.update_data(about_uz=message.text)
    await message.answer("Enter product description in Russian:")
    await state.set_state(ProductAdd.about_ru)

@router.message(IsAdmin(),ProductAdd.about_ru)
async def get_about_ru(message: types.Message, state: FSMContext):
    await state.update_data(about_ru=message.text)
    await message.answer("Enter product description in English:")
    await state.set_state(ProductAdd.about_en)

@router.message(IsAdmin(),ProductAdd.about_en)
async def get_about_en(message: types.Message, state: FSMContext):
    await state.update_data(about_en=message.text)
    await message.answer("Enter product price:")
    await state.set_state(ProductAdd.price)

@router.message(IsAdmin(),ProductAdd.price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await message.answer("Send product image URL:")
    await state.set_state(ProductAdd.image)

@router.message(IsAdmin(),ProductAdd.image)
async def get_image(message: types.Message, state: FSMContext, session : AsyncSession):
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        await state.update_data(image=file_id)
    elif message.text:
        await state.update_data(image=message.text)
    data = await state.get_data()
    # Call add_product function to save to db (example)
    product_id = await add_product(session=session, data=data)
    if product_id:
        text = "✅ Product added with ID:"
        await message.answer(f"{text} {product_id}", reply_markup=await admin_product_keyboard(session=session, chat_id=message.chat.id))
    else:
        await message.answer("❌ Error adding product.",reply_markup=await admin_product_keyboard(session=session, chat_id=message.chat.id))

    await state.clear()