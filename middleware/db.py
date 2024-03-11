from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class UserIdConvertMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
                       ) -> Any:
        res = await handler(event, data)
        print(res)
        return res
