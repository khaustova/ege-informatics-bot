from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .factories import CategoryCallbackFactory
from ..models import Assignment, Category, Results
from ..services.vocabulary import BotEmoji


async def make_menu_keyboard(user_id) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру со всеми категориями заданий и кнопкой выбора 
    случайного режима.
    """
    categories_keyboard_builder = InlineKeyboardBuilder()
    categories_buttons: list[InlineKeyboardButton] = []
    
    for category in await Category.category_manager.get_categories():
        done: int = await Results.objects.filter(
            user__user_id=user_id, 
            category__category=category.category
        ).acount()
        all: int = await Assignment.objects.filter(
            category__category=category.category
        ).acount()
        categories_buttons.append(InlineKeyboardButton(
            text=f'{category.category} ({done}/{all})',
            callback_data=CategoryCallbackFactory(
                category_id=category.id
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
