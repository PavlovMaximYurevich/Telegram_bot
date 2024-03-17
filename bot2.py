import asyncio
import logging
import sqlite3
import time

import aiosqlite
from aiogram import Dispatcher, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

# from telegram.ext import Updater, CommandHandler
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.handlers import AddEvent
from app.keyboards import keyboard
from app.reply_keyboards import yes_or_no_keyboard
from database.engine import create_db, drop_db, sessionmaker

from config import TOKEN_ADMIN_BOT
from middleware.db import DatabaseSession
from database.orm_query import orm_add_event, orm_get_event, orm_get_all_event, not_approved_event, orm_del_event

admin_bot = Bot(token=TOKEN_ADMIN_BOT)
dispatcher = Dispatcher()

engine = create_async_engine('sqlite+aiosqlite:///sqlite.db', echo=True)
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
session = Session()


async def get_from_database(update, context):
    messages = session.query(Message).all().count()
    for msg in messages:
        update.message.reply_text(msg.text)


@dispatcher.callback_query(F.data == 'Отклонить')
async def delete_event(callback: CallbackQuery, session: AsyncSession):
    event_id = callback.data
    await orm_del_event(session, int(event_id))
    await callback.answer("Отклонено!")




@dispatcher.message()
async def not_approved_events(message: Message):
    while True:
        conn = sqlite3.connect('sqlite.db')
        cursor = conn.cursor()

        result = cursor.execute('SELECT * FROM event WHERE approved = "NOT"')

        listt = result.fetchall()

        for event in listt:

            if "NOT" in event:
                await message.answer(str(event[:5]), reply_markup=keyboard)
        break

    time.sleep(5)


async def main_bot_2():
    dispatcher.update.middleware(DatabaseSession(session_pool=sessionmaker))
    await not_approved_events()
    await dispatcher.start_polling(admin_bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main_bot_2())
