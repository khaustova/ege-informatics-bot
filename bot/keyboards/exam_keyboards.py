from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from ..services.vocabulary import BotEmoji


def make_restart_keyboard():
    """
    Создаёт инлайн-клавиатуру, которая прикрепляется к сообщению, когда 
    в выбранном разделе больше нет нерешённых заданий, и которая предлагает
    сбросить прогресс по разделу или вернуться в меню выбора раздела.
    """
    restart_keyboard_builder = InlineKeyboardBuilder()
    restart_keyboard_buttons: list[InlineKeyboardButton] = []
    
    restart_keyboard_buttons.append(InlineKeyboardButton(
        text=f'{BotEmoji.green_checkmark} Да, начать заново!',
        callback_data='restart'
        )
    )
    
    restart_keyboard_buttons.append(InlineKeyboardButton(
        text=f'{BotEmoji.red_cross} Нет, вернуться в меню выбора',
        callback_data='back_to_menu'
        )
    )

    restart_keyboard_builder.row(*restart_keyboard_buttons, width=1)

    return restart_keyboard_builder.as_markup()


def make_exam_menu_keyboards():
    keyboards_builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text='Вернуться в главное меню'),
        KeyboardButton(text='Показать статистику')
    ]
    keyboards_builder.row(*buttons, width=1)
    
    return keyboards_builder.as_markup(resize_keyboard=True)
    
    