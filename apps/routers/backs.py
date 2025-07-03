from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.admin import admin_main_menu_keyboard, admin_category_keyboard, admin_product_keyboard
from apps.keyboards.inline.category import CategoryDetail
from apps.keyboards.inline.product import ProductDetail
from apps.states.admin import AdminMainMenu, ProductAdd
from loader import _
router = Router()

@router.message(IsAdmin() ,F.text.in_(["Back ⬅️","Назад🔙","Ortga🔙"]), AdminMainMenu.product)
@router.message(IsAdmin() ,F.text.in_(["Back ⬅️","Назад🔙","Ortga🔙"]), AdminMainMenu.category)
async def back(message: types.Message, state: FSMContext):
    await message.answer(text="Back ⬅️",reply_markup=await admin_main_menu_keyboard())
    await state.clear()

@router.callback_query(IsAdmin(), CategoryDetail.filter(F.act == "back"))
async def category_back_handler(
        callback: types.CallbackQuery,
        session: AsyncSession
):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text=_("Back to category menu ⬅️"),
        reply_markup=await admin_category_keyboard(
            session=session,
            chat_id=callback.from_user.id
        )
    )

@router.callback_query(IsAdmin(), ProductDetail.filter(F.act == "back"))
async def product_back_handler(
        callback: types.CallbackQuery,
        session: AsyncSession
):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text=_("Back to category menu ⬅️"),
        reply_markup=await admin_product_keyboard(
            session=session,
            chat_id=callback.from_user.id
        )
    )
