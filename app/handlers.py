import logging

import app.keyboards as kb
import app.reply_keyboards as keyb
from telethon.tl.types import InputUser

from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, ShippingQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from Telegram_bot.app.default_keyboard import get_keyboard
from Telegram_bot.app.reply_keyboards import name_telegram, add_event
from Telegram_bot.config import TOKEN
from Telegram_bot.database.orm_query import orm_add_event, orm_get_event, orm_get_all_event

from aiogram import Dispatcher, Bot


router = Router()


class Reg(StatesGroup):
    name = State()
    number_phone = State()


class AddEvent(StatesGroup):
    event_name = State()
    link = State()
    tg_username = State()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет, я могу добавить мероприятие\nЧтобы добавить нажми кнопку ниже",
        reply_markup=get_keyboard(
            "Добавить мероприятие",
            # "Все мероприятия",
            placeholder="Что вас интересует?",
            sizes=(2,)
        ),
    )


@router.message(StateFilter('*'), Command('Отмена'))
@router.message(StateFilter('*'), F.text.casefold() == 'Отмена')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действие отменено", reply_markup=add_event)


@router.message(StateFilter('*'), Command('назад'))
@router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def back_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AddEvent.event_name:
        await message.answer("Предыдущего шага нет")
        return
    previous_step = None
    for step in AddEvent.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_step)
            await message.answer('Вы вернулись к предыдущему шагу')
        previous_step = step


@router.message(StateFilter(None), F.text == "Добавить мероприятие")
async def add_product(message: Message, state: FSMContext):
    await message.answer(
        "Введите название мероприятия", reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddEvent.event_name)


@router.message(AddEvent.event_name, F.text)
async def add_name_product(message: Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await message.answer("Где будет проходить мероприятие?(можно отправить ссылку)")
    await state.set_state(AddEvent.link)


@router.message(AddEvent.link, F.text)
async def add_price_product(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer("Выберите контакт", reply_markup=name_telegram)
    # await message.answer(str(message.user_shared.user_id))
    # await message.answer_contact('Выберите контакт', reply_markup=name_telegram,
    #                              first_name=message.from_user.full_name)
    await state.set_state(AddEvent.tg_username)


@router.message(AddEvent.tg_username)
# async def finish(message: Message, state: FSMContext):
async def finish(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    print(callback)
    user_id = callback.users_shared.user_ids[0]
    # from telethon.sync import TelegramClient

    # from telethon import functions, types
    # api_id = 29478159
    # api_hash ='77d93175bd5dd564694fa6fedaf4bcd6'
    #

    await state.update_data(tg_username=user_id)
    user_data = await state.get_data()
    # await callback.answer(str(user_data))
    # channel_id = '-4116868761'
    #
    #
    # message_id = callback.message_id
    # chat_id = callback.chat.id
    # chat_id = f'-{chat_id}'
    # print("CHAAAAAT", chat_id)
    # print("MESSAGE", message_id)
    # await callback.answer(str(user_data))
    # await callback.answer(message_id)
    # await callback.bot.forward_message(chat_id=channel_id, from_chat_id=chat_id, message_id=message_id)
    # await forward_message(callback, channel_id)
    # await bot.send_message(chat_id)
    # TO_CHAT_ID = 7123407048
    # await bot.send_message(channel_id, str(user_data))
    # await bot.get_chat_administrators(chat_id)
    # await bot.forward_message(TO_CHAT_ID, callback.chat.id, message_id)
    # await bot.forward_message(c, message.chat.id, message.message_id)
    await callback.answer('ожидайте подтверждения')
    await orm_add_event(session, user_data)
    await state.clear()


@router.message(F.text == 'Все мероприятия')
async def get_all_events(message: Message, session: AsyncSession):
    for event in await orm_get_all_event(session):
        await message.answer(f'Мероприятие{event.event_name}\n'
                             f'Ссылка {event.event_link}\n'
                             f'Спикер {event.contact_tg}')




# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.reply(f'Привет {message.from_user.first_name}',
#                         reply_markup=keyb.test_kb)


# @router.message(Command('reg'))
# async def reg_step_one(message: Message, state: FSMContext):
#     await state.set_state(Reg.name)
#     await message.answer('Введите ваше имя')
#
#
# @router.message(Reg.name)
# async def reg_step_two(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Reg.number_phone)
#     await message.answer('Введите номер телефона')
#
#
# @router.message(Reg.number_phone)
# async def reg_step_three(message: Message, state: FSMContext):
#     await state.update_data(number_phone=message.text)
#     data = await state.get_data()
#     await message.answer(f'Регистрация завершена\nИмя: {data.get("name")}\nНомер: {data.get("number_phone")}')
#     await state.clear()


# @router.callback_query(F.data == 'approve')
# async def approve(callback: CallbackQuery):
#     await callback.answer(f'Вы нажали {callback.data}')
#     await callback.message.edit_text('Куку', reply_markup=await kb.inline_cars())


# @router.message(F.text.contains('при'))
# async def test_func(message: Message):
#     await message.answer("Это магический фильтр")


