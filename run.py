import asyncio
import logging

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommandScopeAllPrivateChats

from config import TOKEN
from app.handlers import router
from common.bot_commands_list import private


bot = Bot(token=TOKEN)
dispatcher = Dispatcher()


async def main():
    dispatcher.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private,
                              scope=BotCommandScopeAllPrivateChats()
                              )
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
