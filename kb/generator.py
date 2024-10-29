from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def generate_kb(commands: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for cmd in commands:
        builder.add(KeyboardButton(text=cmd))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
