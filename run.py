import asyncio
import logging

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import Message, BotCommandScopeAllPrivateChats

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from database.engine import create_db, drop_db, sessionmaker
from middleware.db import DatabaseSession
from config import TOKEN, TOKEN_ADMIN_BOT
from app.handlers import router
from common.bot_commands_list import private


bot = Bot(token=TOKEN)
# admin_bot = Bot(token=TOKEN_ADMIN_BOT)
dispatcher = Dispatcher()
dispatcher.include_router(router)


async def on_start_up(bot: Bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()


async def on_shutdown(bot):
    print('Бот не работает')


async def main():
    dispatcher.startup.register(on_start_up)
    dispatcher.shutdown.register(on_shutdown)
    dispatcher.update.middleware(DatabaseSession(session_pool=sessionmaker))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private,
                              scope=BotCommandScopeAllPrivateChats()
                              )
    await dispatcher.start_polling(bot)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
