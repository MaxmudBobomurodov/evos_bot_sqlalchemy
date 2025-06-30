from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.admin import admin_main_menu_keyboard
router = Router()

@router.message(IsAdmin() ,F.text.in_(["Back ⬅️"]))
async def back(message: types.Message, state: FSMContext):
    await message.answer(text="Back ⬅️",reply_markup=await admin_main_menu_keyboard())
    await state.clear()
