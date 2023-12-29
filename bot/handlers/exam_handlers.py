from random import shuffle
from typing import Any
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PollAnswer, FSInputFile
from ..main import bot
from ..models import User, Assignment, Results, Category
from ..keyboards.exam_keyboards import make_restart_keyboard
from ..states.take_exam import TakeExam
from ..services.vocabulary import BotVocabulary
from ..services.send_assignment import send_assignment, end_of_assignment

router = Router()


@router.message(StateFilter(TakeExam.get_question))
async def get_assignment(user_id: int | str, state: FSMContext):
    """
    Определяет задание для пользователя в соответствии с выбранным разделом,
    и, если оно существует, то отправляет его, иначе - уведомляет об этом и 
    предлагает сбросить прогресс по разделу или вернуться в главное меню.
    """
    assignment_data: dict[str, Any] = await state.get_data()

    assignment: Assignment = await Assignment.exam_manager.get_assignment(
            user_id=user_id, 
            category_id=assignment_data['category_id']
        )
      
    if assignment:
        await send_assignment(
            user_id=user_id,
            assignment=assignment, 
            state=state
        )
    else:
        await end_of_assignment(
            user_id=user_id, 
            category_id=assignment_data['category_id'], 
            state=state
        )


@router.poll_answer(StateFilter(TakeExam.get_result))
async def get_result_assignment_poll(poll_answer: PollAnswer, state: FSMContext):
    """
    Обработчик выбора ответа на задание в виде викторины.
    """
    assignment_data: dict[str, Any] = await state.get_data()

    result: bool = True
    if assignment_data['correct_option_id'] != poll_answer.option_ids[0]:
        result = False
    
        
    await Results.objects.acreate(
        user=await User.objects.aget(user_id=poll_answer.user.id),
        question=await Assignment.objects.aget(id=assignment_data['current_question_id']),
        category=await Category.objects.aget(id=assignment_data['category_id']),
        status=result,
    )  

    await state.set_state(TakeExam.get_question)
    await get_assignment(poll_answer.user.id, state)
    
        
@router.message(StateFilter(TakeExam.get_result))
async def get_result_assignment_reply(message: Message, state: FSMContext):
    """
    Обработчик ответа на задание с кратким ответом.
    """
    assignment_data: dict[str, Any] = await state.get_data()
    if assignment_data['current_question_type'] == 'select_one':
        await message.answer(
            text=BotVocabulary.message_poll
        )
    elif assignment_data['current_question_type'] == 'short_reply':

        if message.text ==  assignment_data['correct_answer']:
            result: bool = True
            await message.answer(
                text=BotVocabulary.message_success,
            )
        else:
            result = False
            await message.answer(
                text=BotVocabulary.message_failure,
            )
            
        await Results.objects.acreate(
            user=await User.objects.aget(user_id=message.from_user.id),
            question=await Assignment.objects.aget(id=assignment_data['current_question_id']),
            category=await Category.objects.aget(id=assignment_data['category_id']),
            status=result,
        ) 
    await state.set_state(TakeExam.get_question)
    await get_assignment(message.from_user.id, state)   
