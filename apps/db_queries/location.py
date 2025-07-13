import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_location_(chat_id: int, session: AsyncSession):
    try:
        result = await session.execute(
            select(User.latitude, User.longitude).where(User.chat_id == chat_id)
        )
        coords = result.first()
        if coords:
            return {"latitude": coords[0], "longitude": coords[1]}
        return None
    except Exception as e:
        logging.error(f"Error: {e}")
        return None

async def update_user_location(chat_id: int, latitude: float, longitude: float, session: AsyncSession):
    try:
        await session.execute(
            update(User)
            .where(User.chat_id == chat_id)
            .values(latitude=latitude, longitude=longitude)
        )
        await session.commit()
    except Exception as e:
        await session.rollback()
        logging.error(f"Error: {e}")

