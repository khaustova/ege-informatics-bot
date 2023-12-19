from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_keyboard(width: int, buttons) -> InlineKeyboardMarkup:
    inline_keyboard_builder = InlineKeyboardBuilder()
    inline_buttons: list[InlineKeyboardButton] = []

    for text, callback_data in buttons.items():
        inline_buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=callback_data
            )
        )

    inline_keyboard_builder.row(*inline_buttons, width=width)

    return inline_keyboard_builder.as_markup()
