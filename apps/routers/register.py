from aiogram import Router,types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.states.user import RegisterState
from apps.keyboards.default.user import user_phone_keyboard, user_main_keyboard
from apps.db_queries.user import register


router = Router()

@router.callback_query(RegisterState.language)
async def get_language(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer("Please, share your phone number ☎️", reply_markup=user_phone_keyboard)
    await state.set_state(RegisterState.phone_number)

@router.message(RegisterState.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number,
                            username=message.from_user.username)


    await message.answer("Please, Enter your fullname✍️")
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def get_user_name(message: types.Message, state: FSMContext, session : AsyncSession):
    await state.update_data(name=message.text)

    data = await state.get_data()
    data['chat_id'] = message.from_user.id
    if await register(data=data, session=session):
        await message.answer("you have successfully registered🎉", reply_markup=user_main_keyboard)
    else:
        await message.answer("Please try again later, something went wrong 😔")

    await state.clear()