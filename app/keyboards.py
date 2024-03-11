from aiogram.types import (KeyboardButton,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButtonRequestUser)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import GRAFIK, START_PAKET

# keyboard = ReplyKeyboardMarkup(
#     resize_keyboard=True,
#     keyboard=[
#         [KeyboardButton(text='Подтвердить')],
#         [KeyboardButton(text='Отклонить')],
#         [KeyboardButton(text='About us'), KeyboardButton(text='Контакты')]
#     ],
#     # input_field_placeholder='Выбери текст ниже'
# )

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='approve')],
    [InlineKeyboardButton(text='Отклонить', callback_data='cancel')],
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    # [InlineKeyboardButton(text='Подтвердить')],
    # [InlineKeyboardButton(text='Отклонить')]
    [InlineKeyboardButton(text='График',
                          url=GRAFIK)],
    [InlineKeyboardButton(text='Стартовый пакет',
                          url=START_PAKET)],
])

# cars = ['Lada', 'BMW', 'Volvo']






# async def inline_cars():
#     keyboards = InlineKeyboardBuilder()
#     for car in cars:
#         keyboards.add(InlineKeyboardButton(text=car, callback_data=car))
#     return keyboards.adjust(3).as_markup()
