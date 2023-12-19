from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CategoryCallbackFactory(CallbackData, prefix='category'):
    category_id: int
    
    
class SubcategoryCallbackFactory(CallbackData, prefix='subcategory'):
    subcategory_id: int


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


def make_menu_keyboard(categories):
    categories_keyboard_builder = InlineKeyboardBuilder()
    categories_buttons: list[InlineKeyboardButton] = []
    for category in categories:
        categories_buttons.append(InlineKeyboardButton(
            text=category['category'],
            callback_data=CategoryCallbackFactory(
                category_id=category['id']
                ).pack()
            )
        )
    categories_keyboard_builder.row(*categories_buttons, width=1)   
    return categories_keyboard_builder.as_markup()


def make_subcategory_keyboard(subcategories):
    subcategories_buttons = {}
    for subcategory in subcategories:
        subcategories_buttons[subcategory['subcategory']] = SubcategoryCallbackFactory(
            subcategory_id=subcategory['id']
        ).pack()     
    return make_inline_keyboard(width=1, buttons=subcategories_buttons)

    