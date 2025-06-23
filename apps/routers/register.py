from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.states.user import RegisterState
from apps.keyboards.default.user import user_phone_keyboard, user_main_keyboard
from apps.db_queries.user import register, get_user


router = Router()

@router.message(F.text == "/start")
async def register(message: types.Message, state: FSMContext, session: AsyncSession):
    chat_id = message.from_user.id
    existing_user = await get_user(chat_id, session)
    if existing_user:
        await message.answer("you have already registered ✅", reply_markup=user_main_keyboard)
        await state.clear()
        return
    await message.answer("Please, share your phone number ☎️", reply_markup=user_phone_keyboard)
    await state.set_state(RegisterState.phone_number)

@router.message(RegisterState.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)


    await message.answer("Please, Enter your fullname✍️")
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    data = await state.get_data()
    data['chat_id'] = message.from_user.id
    if register(data=data):
        await message.answer("you have successfully registered🎉", reply_markup=user_main_keyboard)
    else:
        await message.answer("Please try again later, something went wrong 😔")

    await state.clear()