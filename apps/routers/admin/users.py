from aiogram import types, F
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.user import get_user, get_all_users
from loader import _
from apps.filters.is_admin import IsAdmin

router = Router()

@router.message(IsAdmin(), F.text.in_(["Users 👯","Пользователи 👯", "Foydalanuvchilar 👯"]))
async def show_users(message: types.Message, session: AsyncSession):
    users = await get_all_users(session)

    if not users:
        await message.answer(_("No users found👤."))
        return

    text = _("The List of users 👥:\n\n")
    for i, u in enumerate(users, 1):
        text += f"{i}. {u.full_name} | @{u.username or 'no_username'} | {u.language}\n"

    await message.answer(text=text)