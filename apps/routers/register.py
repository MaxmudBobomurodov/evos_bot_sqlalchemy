from aiogram import Router,types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.states.user import RegisterState
from apps.keyboards.default.user import user_phone_keyboard, user_main_keyboard, location_share_keyboard
from apps.db_queries.user import register
from loader import _


router = Router()

@router.callback_query(RegisterState.language)
async def get_language(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(language=call.data, chat_id=call.message.chat.id)

    await call.message.answer(_("Please, share your phone number ☎️", locale=call.data), reply_markup=await user_phone_keyboard(locale=call.data))
    await state.set_state(RegisterState.phone_number)

@router.message(RegisterState.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number,
                            username=message.from_user.username)
    data = await state.get_data()
    language = data.get("language")


    await message.answer(_("Please, Enter your fullname✍️", locale=language))
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    language = data.get("language")

    await message.answer(_("please , share your location", locale=language), reply_markup=await location_share_keyboard(locale=language))
    await state.set_state(RegisterState.location)

@router.message(RegisterState.location)
async def get_location(message: types.Message, state: FSMContext, session : AsyncSession):
    await state.update_data(location=message.location)

    data = await state.get_data()
    language = data.get("language")
    data['chat_id'] = message.from_user.id
    if await register(data=data, session=session):
        await message.answer(_("you have successfully registered🎉", locale=language), reply_markup=await user_main_keyboard(locale=language))
    else:
        await message.answer(_("Please try again later, something went wrong 😔", locale=language))

    await state.clear()