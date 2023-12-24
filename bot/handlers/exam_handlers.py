from typing import Any
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PollAnswer
from aiogram.types import CallbackQuery
from ..main import bot
from ..db_methods import get_assignments_ids
from ..models import User, Assignment, Results, Subcategory
from ..keyboards.exam_keyboards import (
    make_restart_keyboard, 
    make_skip_keyboard,
    make_next_keyboard,
)
from ..states.take_exam import TakeExam
from ..services.exam_services import get_assignment_poll, get_assignment_reply

router = Router()


@router.message(StateFilter(TakeExam.get_question))
async def get_assignment(user_id: int | str, state: FSMContext):
    assignment_data: dict[str, Any] = await state.get_data()
    step: int = assignment_data['step'] + 1
    
    try:
        assignment_id = int(assignment_data['assignments_ids'].split('_')[step])
    except:
        assignment_id = None
        
    if assignment_id:
        assignment: Assignment = await Assignment.objects.aget(id=assignment_id)

        await state.update_data(
            step=step,
            current_question_id=assignment.pk,
            current_question_type=assignment.question_type,
            assignment_number=step
        )   
        
        skip_keyboard = make_skip_keyboard()
        
        if str(assignment.pk) == assignment_data['assignments_ids'].split('_')[-1]:
            skip_keyboard = None
            await state.update_data(is_last_assignment=True)
        
        if assignment.question_type == 'select_one':
            global exam_poll
            exam_poll = await get_assignment_poll(user_id, assignment, skip_keyboard, step, assignment_data['number_of_assignments'])
        elif assignment.question_type == 'short_reply':
            await state.update_data(correct_answer=assignment.correct_answer)
            await get_assignment_reply(user_id, assignment, skip_keyboard)
        
        await state.set_state(TakeExam.get_result)
    else:
        await bot.send_message(
            chat_id=user_id,
            text=f"Вы решили все задания по этой теме.\nХотите удалить текущие результаты и начать заново?",
            reply_markup=make_restart_keyboard()
        )
        await state.set_state(TakeExam.no_more_questions)


@router.poll_answer(StateFilter(TakeExam.get_result))
async def get_result_assignment_poll(poll_answer: PollAnswer, state: FSMContext):
    assignment_data: dict[str, Any] = await state.get_data()
    print(poll_answer)
    result = True
    if exam_poll.poll.correct_option_id != poll_answer.option_ids[0]:
        result = False
        
    await Results.objects.acreate(
        user=await User.objects.aget(user_id=poll_answer.user.id),
        question=await Assignment.objects.aget(id=assignment_data['current_question_id']),
        subcategory=await Subcategory.objects.aget(id=assignment_data['subcategory_id']),
        status=result,
    )  

    if assignment_data['is_last_assignment']:
        await state.set_state(TakeExam.get_question)
        await get_assignment(poll_answer.user.id, state)
    else:
        await state.set_state(TakeExam.next_question) 
        await exam_poll.edit_reply_markup(reply_markup=make_next_keyboard())

        
@router.message(StateFilter(TakeExam.get_result))
async def get_result_assignment_reply(message: Message, state: FSMContext):
    assignment_data: dict[str, Any] = await state.get_data()
    if assignment_data['current_question_type'] == 'select_one':
        await message.answer(
            text='Вам нужно выбрать один из вариантов ответа на поставленный вопрос.'
        )
    elif assignment_data['current_question_type'] == 'short_reply':
        next_keyboard = make_next_keyboard()
        if assignment_data['is_last_assignment']:
            next_keyboard = None

        if message.text ==  assignment_data['correct_answer']:
            result = True
            await message.answer(
                text='Правильно.',
                reply_markup=next_keyboard
            )
        else:
            result = False
            await message.answer(
                text='Неправильно.',
                reply_markup=next_keyboard
            )
            
        await Results.objects.acreate(
            user=await User.objects.aget(user_id=message.from_user.id),
            question=await Assignment.objects.aget(id=assignment_data['current_question_id']),
            subcategory=await Subcategory.objects.aget(id=assignment_data['subcategory_id']),
            status=result,
        ) 
        
        if assignment_data['is_last_assignment']:
            await state.set_state(TakeExam.get_question)
            await get_assignment(message.from_user.id, state)
        else:
            await state.set_state(TakeExam.next_question) 
            await message.edit_reply_markup(reply_markup=make_next_keyboard())
    

@router.callback_query(StateFilter(TakeExam.next_question), F.data=='next')
async def get_next_assignment(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(TakeExam.get_question)
    await get_assignment(callback.from_user.id, state)
    
    
@router.callback_query(StateFilter(TakeExam.get_result), F.data=='skip')
async def skip_assignment(callback: CallbackQuery, state: FSMContext):
    assignment_data = await state.get_data()
    step = assignment_data['step']
    assignments_ids = assignment_data['assignments_ids'].split('_')
    question_id = assignments_ids.pop(step)
    assignments_ids_with_skip = '_'.join(assignments_ids) + '_' + question_id
    
    await state.update_data(
        assignments_ids=assignments_ids_with_skip,
        step=step - 1
    )
    
    await callback.message.delete()    
    await state.set_state(TakeExam.get_question)
    await get_assignment(callback.from_user.id, state)
    

@router.callback_query(StateFilter(TakeExam.no_more_questions), F.data=='restart')
async def restart_exam(callback: CallbackQuery, state: FSMContext):
    assignment_data = await state.get_data()
    await Results.objects.filter(
        user__user_id=callback.from_user.id,
        subcategory__id=assignment_data['subcategory_id']
    ).adelete()
    await callback.message.answer(text='Удалено')
    
    assignments_ids = await get_assignments_ids(
        callback.from_user.id, 
        assignment_data['subcategory_id']
    )
    number_of_assignments = len(assignments_ids.split('_'))
    
    await state.update_data(
        step=-1, 
        assignments_ids=assignments_ids, 
        is_last_assignment=False,
        number_of_assignments=number_of_assignments
    )
    await state.set_state(TakeExam.get_question)
    await get_assignment(callback.from_user.id, state)
