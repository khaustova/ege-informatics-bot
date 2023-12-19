import random
from .builders import make_inline_keyboard
from ..models import Assignment


def make_choices_keyboard(question: Assignment):
    choices_buttons = {}
    choices = [
        {question.choice_1: 'wrong_choice'},
        {question.choice_2: 'wrong_choice'},
        {question.choice_3: 'wrong_choice'},
        {question.correct_answer: 'correct_choice'},
    ]
    random.shuffle(choices)
    
    for choice in choices:
        choices_buttons.update(choice)
    
    return make_inline_keyboard(width=1, buttons=choices_buttons)
    
    
    # choices_keyboard_builder = InlineKeyboardBuilder()
    # choices_buttons: list[InlineKeyboardButton] = {}
    
    # for text, callback_data in choices:
    #     choices_buttons.append(InlineKeyboardButton(
    #         text=text,
    #         callback_data=callback_data
    #         )
    #     )
    
    # random.shuffle(choices_buttons)
    # choices_keyboard_builder.row(*choices_buttons, width=2)
    
    # return choices_keyboard_builder.as_markup()


def make_restart_keyboard():
    restart_buttons = {
        '\U00002705 Да, начать заново!': 'restart',
        '\U0000274C Нет, вернуться в меню выбора': 'exit'
    }
    return make_inline_keyboard(width=1, buttons=restart_buttons)
    