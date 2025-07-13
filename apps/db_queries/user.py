import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_user(chat_id: int, session: AsyncSession):
    try:
        result = await session.execute(select(User).where(User.chat_id == chat_id))
        user = result.scalar_one_or_none()
        return user
    except Exception as e:
        logging.error(e)
        return None

async def get_language(chat_id: int, session: AsyncSession):
    try:
        result = await session.execute(select(User.language).where(User.chat_id == chat_id))
        user = result.scalar_one_or_none()
        return user
    except Exception as e:
        logging.error(e)
        return None


async def register(data: dict, session: AsyncSession):
    try:
        user = User(
            username=data.get("username"),
            full_name=data.get("name"),
            chat_id=data.get("chat_id"),
            language=data.get("language"),
            phone_number=data.get("phone_number"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude")
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user.id
    except Exception as e:
        logging.error(e)
        await session.rollback()
        return None

from sqlalchemy import update

async def update_user_language(user_id: int, language: str, session):
    stmt = (
        update(User)
        .where(User.chat_id == user_id)
        .values(language=language)
    )
    await session.execute(stmt)
    await session.commit()

async def get_all_users(session):
    result = await session.execute(select(User))
    return result.scalars().all()
