from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Order


async def add_order(session: AsyncSession, user_id: int, product_id: int):
    order = Order(user_id=user_id, product_id=product_id)
    session.add(order)
    await session.commit()
