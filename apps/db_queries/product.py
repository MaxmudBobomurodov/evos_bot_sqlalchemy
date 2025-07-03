import logging
from sqlalchemy import select, or_, delete, update
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

async def get_product_by_name(session: AsyncSession, name: str):
    try:
        result = select(Product).where(
            or_(Product.name['uz'].astext == name,
                Product.name['ru'].astext == name,
                Product.name['en'].astext == name
                ))
        result = await session.execute(result)
        product = result.scalars().one_or_none()
        return product
    except Exception as e:
        logging.error(e)
        return None

async def delete_product(session: AsyncSession, product_id: int):
    try:
        result = delete(Product).where(Product.id == product_id)
        await session.execute(result)
        await session.commit()
        return True
    except Exception as e:
        logging.error(e)
        return False

async def get_product_by_id(product_id: int, session: AsyncSession):
    result = await session.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def update_product_name(
        session: AsyncSession,
        product_id: int,
        data: dict
):
    try:
        product = update(Product).where(Product.id == product_id).values(
            name={
                "uz": data['name_uz'],
                "ru": data['name_ru'],
                "en": data['name_en']
            }
        )
        result = await session.execute(product)
        await session.commit()

        if result.rowcount == 0:
            logging.warning(f"No product found with id={product_id} to update.")
            return False

        return True
    except Exception as e:
        logging.error(e)
        await session.rollback()
        return False

async def update_product_about(
        session: AsyncSession,
        product_id: int,
        data: dict
):
    try:
        product = update(Product).where(Product.id == product_id).values(
            about={
                "uz": data['about_uz'],
                "ru": data['about_ru'],
                "en": data['about_en']
            }
        )
        result = await session.execute(product)
        await session.commit()

        if result.rowcount == 0:
            logging.warning(f"No product found with id={product_id} to update.")
            return False

        return True
    except Exception as e:
        logging.error(e)
        await session.rollback()
        return False