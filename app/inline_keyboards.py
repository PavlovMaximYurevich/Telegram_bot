from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def approve_or_cancel_keyboard(*, buttons: dict[str, str]):

    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text,
                                          callback_data=data))

    return keyboard.adjust().as_markup()
