import logging

from aiogram import types
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.product import get_product_by_name, delete_product, get_product_by_id, update_product_name
from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.admin import admin_product_keyboard
from apps.keyboards.inline.product import ProductDetail, admin_product_detail_keyboard, admin_product_update_keyboard
from apps.states.admin import AdminMainMenu, ProductUpdate
from loader import _

router = Router()


@router.callback_query(IsAdmin(), AdminMainMenu.product, ProductDetail.filter(F.act=="delete_product"))
async def admin_category_detail_handler(
        call: CallbackQuery, session: AsyncSession,
        callback_data: ProductDetail
):
    if await delete_product(
            session=session,
            product_id=callback_data.product_id
    ):
        text =_("Delete category id:")
        await call.answer(text=f"{text} {callback_data.product_id}",show_alert=True)
        await call.message.delete()
        text = "Category menu"
        await call.message.answer(
            text=text,
            reply_markup=await admin_product_keyboard(
                session=session, chat_id=call.message.chat.id
            ))
    else:
        await call.answer(text="Something went wrong ❌")

@router.callback_query(IsAdmin(),AdminMainMenu.product, ProductDetail.filter(F.act=="update_product"))
async def admin_product_update_handler(
        callback: types.CallbackQuery,
        session: AsyncSession
):
    data = ProductDetail.unpack(callback.data)
    product = await get_product_by_id(session=session, product_id=data.product_id)

    await callback.message.answer(text=_("Choose action:"),
                         reply_markup=await
                         admin_product_update_keyboard(
                             product=product
                             ))

@router.callback_query(IsAdmin(),AdminMainMenu.product, ProductDetail.filter(F.act=="update_name"))
async def admin_product_update_handler(
        callback: types.CallbackQuery,
        session: AsyncSession,
        state: FSMContext
):
    data = ProductDetail.unpack(callback.data)
    await state.update_data(product_id=data.product_id)

    await callback.message.answer(text=_("enter new category name in uzbek:"),reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductUpdate.name_uz)

@router.message(IsAdmin(), ProductUpdate.name_uz)
async def admin_product_update_handler(message: types.Message, state: FSMContext):
    await state.update_data(name_uz=message.text)
    text = "Enter new name in russian:"
    await message.answer(text=text,reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductUpdate.name_ru)

@router.message(IsAdmin(), ProductUpdate.name_ru)
async def admin_product_update_handler(message: types.Message, state: FSMContext):
    await state.update_data(name_ru=message.text)
    text = "Enter new name in english:"
    await message.answer(text=text,reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductUpdate.name_en)

@router.message(IsAdmin(), ProductUpdate.name_en)
async def update_product_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(name_en=message.text)
    data = await state.get_data()
    product_id = data.get("product_id")
    if product_id is None:
        await message.answer("Error , product id has not found❌")
        return
    logging.info(f"Updating product ID: {product_id}")
    updated = await update_product_name(session=session, product_id=product_id, data=data)

    if updated:
        text =_("Product name is updated✅")
    else:
        text = _("Something went wrong, please try again later❌")
    await message.answer(text=text,
                         reply_markup=await admin_product_keyboard(
                             session=session,chat_id=message.chat.id
                         ))
    await state.set_state(AdminMainMenu.product)


@router.message(IsAdmin(), AdminMainMenu.product)
async def accept_all_messages_product_handler(
            message: types.Message,
            session: AsyncSession
):

    product = await get_product_by_name(session=session, name=message.text)
    if product:
        text = f"""
Uzbek: {product.name['uz']}
Russian: {product.name['ru']}
English: {product.name['en']}
 """
        await message.answer(text=text,
                             reply_markup=await admin_product_detail_keyboard(
                            product=product
                        ))