import logging
from asyncio import run

from aiogram import Bot

from apps.middlewares.subscription import SubscribeMiddleware
from apps.utils.commands import set_my_commands
from core.config import DEVELOPER
from apps.middlewares.db_session import DbSessionMiddleware
from apps.middlewares.language import LanguageMiddleware
from apps.routers import register, start, feedback, backs
from loader import bot, dp, i18n
from apps.routers.admin import category, product, product_delete, product_extra_functions


async def startup(bot: Bot):
    await set_my_commands(bot)
    await bot.send_message(text="Bot start to work", chat_id=DEVELOPER)


async def shutdown(bot: Bot):
    await bot.send_message(text="Bot stopped", chat_id=DEVELOPER)


async def main():
    dp.include_router(router=start.router)


    # admin routers
    dp.include_router(router=backs.router)
    dp.include_router(router=product.router)
    dp.include_router(router=category.router)
    dp.include_router(router=product_delete.router)
    dp.include_router(router=product_extra_functions.router)

    # user routers
    dp.include_router(router=register.router)
    dp.include_router(router=feedback.router)


    dp.message.middleware.register(DbSessionMiddleware())
    dp.callback_query.middleware.register(DbSessionMiddleware())
    dp.message.middleware.register(LanguageMiddleware(i18n=i18n))
    dp.message.middleware.register(SubscribeMiddleware())
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot, polling_timeout=0)


if __name__ == '__main__':
    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.ERROR
    )
    logging.getLogger("aiogram.event").setLevel(logging.ERROR)
    run(main())