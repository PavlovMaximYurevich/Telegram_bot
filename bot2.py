import asyncio
import logging
import sqlite3
import time

import aiosqlite
from aiogram import Dispatcher, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter

# from telegram.ext import Updater, CommandHandler
from sqlalchemy import create_engine, select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.handlers import AddEvent
from app.inline_keyboards import approve_or_cancel_keyboard
from app.keyboards import keyboard
from app.reply_keyboards import yes_or_no_keyboard
from database.engine import create_db, drop_db, sessionmaker

from config import TOKEN_ADMIN_BOT
from database.models import Event
from middleware.db import DatabaseSession
from database.orm_query import orm_add_event, orm_get_event, orm_get_all_event, orm_del_event, \
    orm_update_status

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


# @router.message(F.text == 'Все мероприятия')
# async def get_all_events(message:Message, session: AsyncSession):
#     for event in await orm_get_all_event(session):
#         await message.answer(f'Мероприятие{event.event_name}\n'
#                              f'Ссылка {event.event_link}\n'


# @dispatcher.callback_query


@dispatcher.message(CommandStart())
async def update_status(message: Message, session: AsyncSession):
    while True:

        for event in await orm_get_all_event(session):
            if event.approved == "NOT":
                await message.answer(f'Мероприятие {event.event_name}\n'
                                     f'Ссылка {event.event_link}\n'
                                     f'Спикер {event.contact_tg}',
                                     reply_markup=approve_or_cancel_keyboard(
                                         buttons={
                                             "Подтвердить": f'approve_{event.id}',
                                             "Отклонить": f'deny_{event.id}'})
                                     )

        break

    time.sleep(5)


@dispatcher.callback_query(StateFilter(None), (F.data.startswith('approve_') | F.data.startswith('deny_')))
async def approve_event(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    # print(callback)
    event_id = callback.data.split("_")[-1]
    event_status = callback.data.split("_")[0]

    if event_status == 'approve':
        user_data = {'approved': event_status}
        await orm_update_status(session,  int(event_id), user_data)
        await callback.answer('Мероприятие записано!')
    if event_status == 'deny':
        user_data = {'approved': event_status}
        await orm_update_status(session, int(event_id), user_data)
        await callback.answer('Мероприятие отклонено!')
        # await callback.message.answer('Мероприятие отклонено!', reply_markup=ReplyKeyboardRemove())




async def main_bot_2():
    dispatcher.update.middleware(DatabaseSession(session_pool=sessionmaker))
    # await orm_update_status()
    await dispatcher.start_polling(admin_bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main_bot_2())

# @admin_router.callback_query(F.data.startswith("delete_"))
# async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
#     product_id = callback.data.split("_")[-1]
#     await orm_delete_product(session, int(product_id))
#
#     await callback.answer("Товар удален")
#     await callback.message.answer("Товар удален!")


# @dispatcher.message(AddEvent.tg_username)
# async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
#     if message.text and message.text == ".":
#         await state.update_data(image=AddProduct.product_for_change.image)
#
#     else:
#         await state.update_data(image=message.photo[-1].file_id)
#     data = await state.get_data()
#     try:
#         if AddProduct.product_for_change:
#             await orm_update_product(session, AddProduct.product_for_change.id, data)
#         else:
#             await orm_add_product(session, data)
#         await message.answer("Товар добавлен/изменен", reply_markup=ADMIN_KB)
#         await state.clear()
#
#     except Exception as e:
#         await message.answer(
#             f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет",
#             reply_markup=ADMIN_KB,
#         )
#         await state.clear()
#
#     AddProduct.product_for_change = None
