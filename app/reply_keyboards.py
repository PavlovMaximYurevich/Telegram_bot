from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType, \
    KeyboardButtonRequestUser
from aiogram.utils.keyboard import ReplyKeyboardBuilder

name_telegram = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Выберите пользователя', request_user=KeyboardButtonRequestUser(request_id=1))]
    ]
)


button = KeyboardButtonRequestUser(request_id=1)


add_event = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Добавить мероприятие')]
    ]
)


start_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Меню'), KeyboardButton(text='О магазине')],
        [KeyboardButton(text='Доставка'), KeyboardButton(text='Варианты оплаты')],
    ]
)


test_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Создать опрос', request_poll=KeyboardButtonPollType(type="Квиз"))],
        [KeyboardButton(text='Название мероприятия')],
        [
            KeyboardButton(text="Отправить номер", request_contact=True),
            KeyboardButton(text="Отправить локацию", request_location=True),
        ],
        [
            KeyboardButton(text='Контакт ТГ', request_user=KeyboardButtonRequestUser(request_id=5)),
            # KeyboardButton(text="Отправить локацию", request_location=True),
        ]
    ]
)


# del_keyboard = ReplyKeyboardRemove()
