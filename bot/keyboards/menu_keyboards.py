from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .factories import CategoryCallbackFactory
from ..db_methods import get_categories
from ..models import Results, Assignment
from ..services.vocabulary import BotEmoji


async def make_menu_keyboard(user_id) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру со всеми категориями заданий и кнопкой выбора 
    случайного режима.
    """
    categories_keyboard_builder = InlineKeyboardBuilder()
    categories_buttons: list[InlineKeyboardButton] = []
    
    categories = await get_categories() 
    for category in categories:
        done = await Results.objects.filter(
            user__user_id=user_id, 
            category__category=category['category']
        ).acount()
        all = await Assignment.objects.filter(
            category__category=category['category']
        ).acount()
        categories_buttons.append(InlineKeyboardButton(
            text=f'{category["category"]} ({done}/{all})',
            callback_data=CategoryCallbackFactory(
                category_id=category['id']
                ).pack()
            )
        )
        
    categories_buttons.append(InlineKeyboardButton(
        text=f'{BotEmoji.dice} Случайно',
        callback_data='random'
        )
    )
    categories_keyboard_builder.row(*categories_buttons, width=1)   
    return categories_keyboard_builder.as_markup()
