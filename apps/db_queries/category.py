import logging

from sqlalchemy import select, or_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category


async def add_category(session: AsyncSession, data: dict):
    try:
        category = Category(
            name={
                "uz": data["name_uz"],
                "ru": data["name_ru"],
                "en": data["name_en"]
            }
        )
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category.id
    except Exception as e:
        logging.error(e)
        await session.rollback()
        return None

async def get_categories(session: AsyncSession):
    try:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        return categories
    except Exception as e:
        logging.error(e)
        return None

async def get_category_by_name(session: AsyncSession, name: str):
    try:
        result = select(Category).where(
            or_(Category.name['uz'].astext == name,
                Category.name['ru'].astext == name,
                Category.name['en'].astext == name
                ))
        result = await session.execute(result)
        category = result.scalars().one_or_none()
        return category
    except Exception as e:
        logging.error(e)
        return None

async def delete_category(session: AsyncSession, category_id: int):
    try:
        result = delete(Category).where(Category.id == category_id)
        await session.execute(result)
        await session.commit()
        return True
    except Exception as e:
        logging.error(e)
        return False

async def get_category_by_id(category_id: int, session: AsyncSession):
    result = await session.execute(
        select(Category).where(Category.id == category_id)
    )
    return result.scalar_one_or_none()

async def update_category(session: AsyncSession, category_id: int, data: dict):
    try:
        category = update(Category).where(Category.id == category_id).values(
            name={
                "uz": data["name_uz"],
                "ru": data["name_ru"],
                "en": data["name_en"]
            }
        )
        result = await session.execute(category)
        await session.commit()

        if result.rowcount == 0:
            logging.warning(f"No category found with id={category_id} to update.")
            return False

        return True
    except Exception as e:
        logging.error(e)
        await session.rollback()
        return False