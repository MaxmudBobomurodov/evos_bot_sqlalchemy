from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.product import add_product
from apps.keyboards.default.admin import admin_product_keyboard
from apps.filters.is_admin import IsAdmin
from apps.states.admin import ProductAdd

router = Router()
@router.message(IsAdmin(), F.text.in_(["Products 🍴","Продукция 🍴","Mahsulotlar 🍴"]))
async def admin_category_handler(message: types.Message, session: AsyncSession):
    text = "product menu "
    await message.answer(text=text,
    reply_markup=await admin_product_keyboard(session=session, chat_id=message.chat.id))


@router.message(IsAdmin(), F.text.in_(["Add product🍴","Mahsulot qo'shish🍴","Добавить категорию 🍴"]))
async def add_category_handler(message: types.Message, state: FSMContext):
    text = "Enter product name in uzbek"
    await message.answer(text=text,
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

@router.message(ProductAdd.name_en)
async def get_name_en(message: types.Message, state: FSMContext):
    await state.update_data(name_en=message.text)
    await message.answer("Enter product description in Uzbek:")
    await state.set_state(ProductAdd.about_uz)

@router.message(ProductAdd.about_uz)
async def get_about_uz(message: types.Message, state: FSMContext):
    await state.update_data(about_uz=message.text)
    await message.answer("Enter product description in Russian:")
    await state.set_state(ProductAdd.about_ru)

@router.message(ProductAdd.about_ru)
async def get_about_ru(message: types.Message, state: FSMContext):
    await state.update_data(about_ru=message.text)
    await message.answer("Enter product description in English:")
    await state.set_state(ProductAdd.about_en)

@router.message(ProductAdd.about_en)
async def get_about_en(message: types.Message, state: FSMContext):
    await state.update_data(about_en=message.text)
    await message.answer("Enter product price:")
    await state.set_state(ProductAdd.price)

@router.message(ProductAdd.price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await message.answer("Send product image URL:")
    await state.set_state(ProductAdd.image)

@router.message(ProductAdd.image)
async def get_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.text)
    await message.answer("Enter category ID:")
    await state.set_state(ProductAdd.category_id)

@router.message(ProductAdd.category_id)
async def get_category_id(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(category_id=int(message.text))
    data = await state.get_data()

    # Call add_product function to save to db (example)
    product_id = await add_product(session=session, data=data)

    if product_id:
        text = "✅ Product added with ID:"
        await message.answer(f"{text} {product_id}", reply_markup=await admin_product_keyboard(session=session, chat_id=message.chat.id))
    else:
        await message.answer("❌ Error adding product.",reply_markup=await admin_product_keyboard(session=session, chat_id=message.chat.id))

    await state.clear()