import asyncio
import time

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, ShippingQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.default_keyboard import get_keyboard
from app.reply_keyboards import name_telegram, add_event
from database.orm_query import orm_add_event, orm_get_event, orm_get_all_event

from aiogram import Dispatcher, Bot


router = Router()


class Reg(StatesGroup):
    name = State()
    number_phone = State()


class AddEvent(StatesGroup):
    event_name = State()
    link = State()
    tg_username = State()
    approved = State()
    # user_chat_id = State()


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

# @router.message(F.text)
# async def user_message(message:Message, bot: Bot):
#     if message.text:
#         # print(message.text)
#         await bot.send_message(chat_id=message.text, text="Одобрено")



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
    await state.set_state(AddEvent.tg_username)


@router.message(AddEvent.tg_username)
async def finish(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    # print(callback.chat.id)
    user_id = callback.users_shared.user_ids[0]
    # your_user_id = callback.chat.id

    await state.update_data(tg_username=user_id)
    # await state.update_data(approved)
    # await state.update_data(user_chat_id=your_user_id)
    user_data = await state.get_data()
    print(user_data)
    # await callback.send_message(chat_id=5831896871, text=f'{your_user_id}#Привет')
    # await bot.send_message(chat_id=7123407048, text=f'{your_user_id}')
    # await bot.send_message(chat_id=7123407048, text="Ждет одобрения")
    await callback.answer('ожидайте подтверждения')
    await orm_add_event(session, user_data)
    await state.clear()

    while True:

            for event in await orm_get_all_event(session):
                if event.approved != "NOT":
                    if event.id == user_data.get('id'):
                        print('Изменился статус')
                    # await callback.answer(f'Мероприятие {event.event_name}\n'
                    #                      f'Ссылка {event.event_link}\n'
                    #                      f'Спикер {event.contact_tg}',
                    #                      reply_markup=approve_or_cancel_keyboard(
                    #                          buttons={
                    #                              "Подтвердить": f'approve_{event.id}',
                    #                              "Отклонить": f'deny_{event.id}'})
                    #                      )

            break

        # time.sleep(5)
    await asyncio.sleep(5)


@router.message(F.text == 'Все мероприятия')
async def get_all_events(message: Message, session: AsyncSession):
    for event in await orm_get_all_event(session):
        await message.answer(f'Мероприятие{event.event_name}\n'
                             f'Ссылка {event.event_link}\n'
                             f'Спикер {event.contact_tg}')



