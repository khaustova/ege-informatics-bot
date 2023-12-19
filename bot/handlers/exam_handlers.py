from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from ..main import dp, bot
from ..models import User, Assignment, Results
from ..db_methods import get_question
from ..keyboards.exam_keyboards import (
    make_choices_keyboard, 
    make_restart_keyboard, 
)

router = Router()


@dp.callback_query(F.data == 'wrong_choice')
async def wrong_choice(callback: CallbackQuery):
    await callback.answer(text='Не расстраивайся!')
    
    await Results.objects.acreate(
        user=await User.objects.aget(user_id=callback.from_user.id),
        question=await Assignment.objects.aget(question=callback.message.text),
        status=False,
    )

    await create_exam(callback.message.chat.id, callback.from_user.id)


@dp.callback_query(F.data == 'correct_choice')
async def correct_choice(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'{callback.message.text}\n\nВаш ответ: {callback.data}',
        reply_markup=None
    )

    await callback.answer(text='Молодец!')
    
    await Results.objects.acreate(
        user=await User.objects.aget(user_id=callback.from_user.id),
        question=await Assignment.objects.aget(question=callback.message.text),
        status=True,
    )

    await create_exam(callback.message.chat.id, callback.from_user.id)


@router.message(Command(commands=['quiz']))   
async def create_exam(chat_id, user_id):
    question = await get_question(user_id)
    
    if question:
        await bot.send_message(
            chat_id=chat_id,
            text=question.question,
            reply_markup=make_choices_keyboard(question)
        )
    else:
        result = Results.objects.filter(user__user_id=user_id)
        all_answered = await result.acount()
        correct_answered = await result.filter(status=True).acount()
        await bot.send_message(
            chat_id=chat_id,
            text=f"Вы решили все задания по этой теме с результатом {correct_answered} из {all_answered}.\nХотите удалить текущие результаты и начать заново?",
            reply_markup=make_restart_keyboard()
        )
