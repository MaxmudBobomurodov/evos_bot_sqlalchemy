import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from core.config import CHANNELS
from loader import bot, _
from aiogram.enums import ChatMemberStatus as CHatS


class SubscribeMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        user_id = event.from_user.id

        try :

            not_joined = list()
            for channel in CHANNELS:
                member = await bot.get_chat_member(chat_id=channel['chat_id'], user_id=user_id)
                if member.status not in [CHatS.CREATOR, CHatS.ADMINISTRATOR, CHatS.MEMBER]:
                    not_joined.append(channel)


            if len(not_joined) == 0:
                return await handler(event, data)

            text = ""
            warming = _("Please subscribe this channels \n")
            text += warming
            for channel in not_joined:
                text += f"{channel['name']} -> {channel['link']}\n"
            await bot.send_message(text=text, chat_id=user_id)
            return None
        except Exception as e:
            logging.error(e)
            return await handler(event, data)