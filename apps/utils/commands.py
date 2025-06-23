from aiogram import Bot
from aiogram.types import BotCommand


async def set_my_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start to work 🚀")
    ]
    await bot.set_my_commands(commands=commands)
