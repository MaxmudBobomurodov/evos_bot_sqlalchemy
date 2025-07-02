import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product

async def add_product(session: AsyncSession, data: dict):
    try:
        product = Product(
    name={
        "uz": data['name_uz'],
        "ru": data['name_ru'],
        "en": data['name_en']
    },
    about={
        "uz": data['about_uz'],
        "ru": data['about_ru'],
        "en": data['about_en']
    },
    price=data['price'],
    image=data['image'],
    category_id=data['category_id']
)
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product.id
    except Exception as e:
        logging.error(e)
        await session.rollback()
        return None


async def get_product(session: AsyncSession):
    try:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        return products
    except Exception as e:
        logging.error(e)
        return None