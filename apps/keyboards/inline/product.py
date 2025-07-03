from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from loader import _

class ProductDetail(CallbackData, prefix="product_detail"):
    act: str
    product_id: int

async def admin_product_detail_keyboard(product):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=_("Delete❌"), callback_data = ProductDetail(
            act= "delete_product",product_id=product.id).pack()),
        InlineKeyboardButton(text=_("Update✅"), callback_data = ProductDetail(
            act= "update_product",product_id=product.id).pack())
    ]])


async def admin_product_update_keyboard(product):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Update name ✍️"), callback_data = ProductDetail(
                act= "update_name",product_id=product.id).pack()),
            InlineKeyboardButton(text=_("update about👀"), callback_data=ProductDetail(
                act="update_about", product_id=product.id).pack())
        ],
        [
            InlineKeyboardButton(text=_("Edit price 💸"), callback_data=ProductDetail(
                act="update_price", product_id=product.id).pack()),
            InlineKeyboardButton(text=_("Edit image 🖼"), callback_data=ProductDetail(
                act="update_image", product_id=product.id).pack())
        ],
        [
            InlineKeyboardButton(text=_("Change category 👣"), callback_data=ProductDetail(
                act="update_category", product_id=product.id).pack()),
            InlineKeyboardButton(text=_("Back⬅️"), callback_data=ProductDetail(
                act="back", product_id=product.id).pack())
        ]
    ])
