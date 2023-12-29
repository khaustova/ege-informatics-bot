from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .factories import StatisticCategoryCallbackFactory
from ..models import Assignment, Category, Results
from ..services.vocabulary import BotEmoji


async def make_statistics_keyboard(user_id: int | str) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру со всеми категориями заданий и кнопкой выбора 
    случайного режима.
    """
    categories_keyboard_builder = InlineKeyboardBuilder()
    categories_buttons: list[InlineKeyboardButton] = []
    
    for category in await Category.category_manager.get_categories() :
        done = await Results.objects.filter(
            user__user_id=user_id, 
            category__category=category.category
        ).acount()
        success = await Results.objects.filter(
            user__user_id=user_id, 
            category__category=category.category,
            status=True
        ).acount()
        all = await Assignment.objects.filter(
            category__category=category.category
        ).acount()
        categories_buttons.append(InlineKeyboardButton(
            text=f'{category.category}',
            callback_data='pass'
            )
        )
        categories_buttons.append(InlineKeyboardButton(
            text=f'{done} ( {success} {BotEmoji.green_checkmark} ) из {all}',
            callback_data='pass'
            )
        )
        categories_buttons.append(InlineKeyboardButton(
            text=f'{BotEmoji.red_cross} Сбросить',
            callback_data=StatisticCategoryCallbackFactory(
                category_id=category.id
                ).pack()
            )
        )

    categories_keyboard_builder.row(*categories_buttons, width=3)   
    return categories_keyboard_builder.as_markup()
