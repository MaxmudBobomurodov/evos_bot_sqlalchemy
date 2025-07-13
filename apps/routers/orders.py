from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from apps.db_queries.orders import add_order
from apps.db_queries.user import get_user
from core.models import Product, Order

router = Router()


@router.callback_query()
async def handle_product_callback(callback: CallbackQuery, session: AsyncSession):
    user = await get_user(session=session, chat_id=callback.from_user.id)
    lang = user.language or "en"

    product_id = int(callback.data)
    product = await session.get(Product, product_id)

    if not product:
        await callback.answer("Product not found ❌ .")
        return


    await add_order(session=session, user_id=user.id, product_id=product_id)

    # Tilga qarab xabar
    product_name = product.name.get(lang, product.name.get("en", "Unnamed"))
    await callback.message.answer(f"✅ {product_name} added to your orders.")
    await callback.answer()

@router.message(F.text == "My Orders📋")
async def show_orders(message: Message, session: AsyncSession):
    user = await get_user(session=session, chat_id=message.chat.id)
    lang = user.language or "en"

    result = await session.execute(
        select(Order).where(Order.user_id == user.id).options(selectinload(Order.product))
    )
    orders = result.scalars().all()

    if not orders:
        await message.answer("You have no orders yet 📭 .")
        return

    lines = ["🧾 Your Orders:\n"]
    total = 0
    for i, order in enumerate(orders, start=1):
        product = order.product
        name = product.name.get(lang, product.name.get("en", "Unnamed"))
        qty = order.quantity
        price = product.price
        sum_price = price * qty
        total += sum_price

        lines.append(f"{i}. {name} — {qty} ta × {price} = {sum_price} so'm")

    lines.append(f"\n🧮 Total: {total} so'm")
    await message.answer("\n".join(lines))
