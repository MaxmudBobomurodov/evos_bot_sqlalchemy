from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import DEVELOPER
from apps.keyboards.default.user import user_main_keyboard
from apps.db_queries.user import get_user
from apps.states.user import Feedback
from loader import _
router = Router()

@router.message(F.text.in_(["Send feedback ✍️","Отправить отзыв ✍️","Izoh qoldiring ✍️"]))
async def send_feedback(message: types.Message, state: FSMContext):
    text = _("Please enter your feedback")
    await message.answer(text=text, reply_markup=await user_main_keyboard())
    await message.answer(text=_("send your feedback:"), reply_markup=await user_main_keyboard())

    await state.set_state(Feedback.feedback)

@router.message(Feedback.feedback)
async def get_feedback(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user = await get_user(chat_id=message.chat.id, session=session)
    feedback = f"""
User: {message.from_user.mention_html(f'{user.full_name}')}
Feedback: {message.text}
    """
    await bot.send_message(text=feedback, chat_id=DEVELOPER)


    text = _("Your feedback is sent successfully ✅")
    await message.answer(text=text, reply_markup=await user_main_keyboard())
    await state.clear()