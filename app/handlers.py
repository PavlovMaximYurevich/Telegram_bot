import logging

import app.keyboards as kb
import app.reply_keyboards as keyb

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from Telegram_bot.app.default_keyboard import get_keyboard
from Telegram_bot.app.reply_keyboards import name_telegram, add_event

router = Router()


class Reg(StatesGroup):
    name = State()
    number_phone = State()


class AddProduct(StatesGroup):
    name_product = State()
    description = State()
    price = State()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Добавить мероприятие",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
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
    if current_state == AddProduct.name_product:
        await message.answer("Предыдущего шага нет")
        return
    previous_step = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_step)
            await message.answer('Вы вернулись к предыдущему шагу')
        previous_step = step


@router.message(StateFilter(None), F.text == "Добавить мероприятие")
async def add_product(message: Message, state: FSMContext):
    await message.answer(
        "Введите название мероприятия", reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name_product)


@router.message(AddProduct.name_product, F.text)
async def add_name_product(message: Message, state: FSMContext):
    await state.update_data(name_product=message.text)
    await message.answer("Введите ссылку локации")
    await state.set_state(AddProduct.description)


@router.message(AddProduct.description, F.text)
async def add_price_product(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Выберите контакт", reply_markup=name_telegram)
    # await message.answer(str(message.user_shared.user_id))
    # await message.answer_contact('Выберите контакт', reply_markup=name_telegram,
    #                              first_name=message.from_user.full_name)
    await state.set_state(AddProduct.price)


@router.message(AddProduct.price)
# async def finish(message: Message, state: FSMContext):
async def finish(callback: CallbackQuery, state: FSMContext):
    user_id = callback.users_shared.user_ids[0]
    # ss = user_id.from_user
    # print(ss)

    await state.update_data(price=user_id)
    user_data = await state.get_data()
    await callback.answer(str(user_data))
    await state.clear()


@router.message(F.text == 'тест')
async def testing_middleware(message: Message):
    pass











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
