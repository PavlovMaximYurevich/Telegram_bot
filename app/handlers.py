import logging

import app.keyboards as kb
import app.reply_keyboards as keyb

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


router = Router()


class Reg(StatesGroup):
    name = State()
    number_phone = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет {message.from_user.first_name}',
                        reply_markup=keyb.test_kb)


@router.message(Command('reg'))
async def reg_step_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя')


@router.message(Reg.name)
async def reg_step_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number_phone)
    await message.answer('Введите номер телефона')


@router.message(Reg.number_phone)
async def reg_step_three(message: Message, state: FSMContext):
    await state.update_data(number_phone=message.text)
    data = await state.get_data()
    await message.answer(f'Регистрация завершена\nИмя: {data.get("name")}\nНомер: {data.get("number_phone")}')
    await state.clear()


# @router.callback_query(F.data == 'approve')
# async def approve(callback: CallbackQuery):
#     await callback.answer(f'Вы нажали {callback.data}')
#     await callback.message.edit_text('Куку', reply_markup=await kb.inline_cars())


@router.message(F.text.contains('при'))
async def test_func(message: Message):
    await message.answer("Это магический фильтр")
