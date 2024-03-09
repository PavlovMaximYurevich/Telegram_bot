import asyncio
import logging

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import TOKEN
from app.handlers import router

bot = Bot(token=TOKEN)

dispatcher = Dispatcher()


async def main():
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
