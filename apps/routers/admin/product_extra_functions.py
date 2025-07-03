import logging

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.product import update_product_about, get_product_by_id
from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.admin import admin_product_keyboard
from apps.keyboards.inline.product import ProductDetail
from apps.states.admin import AdminMainMenu, ProductUpdateAbout
from core.models import Product
from loader import _

router = Router()
@router.callback_query(
    IsAdmin(),
    AdminMainMenu.product,
    ProductDetail.filter(F.act=="update_about"
    ))
async def admin_product_update_about_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession
):
    data = ProductDetail.unpack(callback.data)
    await state.update_data(product_id=data.product_id)
    product = await get_product_by_id(product_id=data.product_id, session=session)
    about = product.about or {}

    await state.update_data(
        product_id=data.product_id,
        old_about_uz=about.get("uz", ""),
        old_about_ru=about.get("ru", ""),
        old_about_en=about.get("en", "")
    )

    await callback.message.answer(
        text=f"Old about sections :\n"
             f" English --> {about.get('en', 'unnamed')}\n"
             f" Russian --> {about.get('ru', 'unnamed')}\n"
             f" Uzbek --> {about.get('uz', 'yoq')}\n\n"
             f"Enter new about section in uzbek:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ProductUpdateAbout.about_uz)

@router.message(IsAdmin(), ProductUpdateAbout.about_uz)
async def admin_product_update_about_handler(message: types.Message, state: FSMContext):
    await state.update_data(about_uz=message.text)
    text = "Enter new about section in russian:"
    await message.answer(text=text,reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductUpdateAbout.about_ru)

@router.message(IsAdmin(), ProductUpdateAbout.about_ru)
async def admin_product_update_about_handler(message: types.Message, state: FSMContext):
    await state.update_data(about_ru=message.text)
    text = "Enter new about section in english:"
    await message.answer(text=text,reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductUpdateAbout.about_en)

@router.message(IsAdmin(), ProductUpdateAbout.about_en)
async def admin_product_update_about(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(about_en=message.text)
    data = await state.get_data()
    product_id = data.get("product_id")
    if product_id is None:
        await message.answer(text=_("Error , product id has not found❌"))
        return
    logging.info(f"Updating product ID: {product_id}")
    updated = await update_product_about(
        session=session,
        product_id=product_id,
        data=data
    )

    if updated:
        text =_("Product about section is updated✅")
    else:
        text = _("Something went wrong, please try again later❌")
    await message.answer(text=text,
                         reply_markup=await admin_product_keyboard(
                             session=session,chat_id=message.chat.id
                         ))
    await state.set_state(AdminMainMenu.product)