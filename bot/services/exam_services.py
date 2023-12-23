from random import shuffle
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup
from ..main import bot
from ..models import Assignment


async def get_assignment_poll(
    user_id: int | str, 
    assignment: Assignment, 
    skip_keyboard: InlineKeyboardMarkup | None
) -> Message:
    options=[
        assignment.choice_1, 
        assignment.choice_2,
        assignment.choice_3,
        assignment.correct_answer
    ]
    shuffle(options)
    exam_poll = await bot.send_poll(
        chat_id=user_id,
        question=assignment.question,
        options=options,
        type='quiz',
        correct_option_id=options.index(assignment.correct_answer),
        is_anonymous=False,
        reply_markup=skip_keyboard
    )
    return exam_poll


async def get_assignment_reply(
    user_id: int | str, 
    assignment: Assignment, 
    skip_keyboard: InlineKeyboardMarkup | None
):
    await bot.send_message(
        chat_id=user_id,
        text=assignment.question,
        reply_markup=skip_keyboard,
    )
