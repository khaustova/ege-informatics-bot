from random import shuffle
from typing import Any
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PollAnswer, CallbackQuery, FSInputFile
from ..main import bot
from ..db_methods import get_assignments_ids, get_categories
from ..models import User, Assignment, Results, Category
from ..keyboards.exam_keyboards import make_restart_keyboard
from ..keyboards.menu_keyboards import make_menu_keyboard
from ..states.take_exam import TakeExam
from ..services.vocabulary import BotVocabulary

router = Router()


@router.message(StateFilter(TakeExam.get_question))
async def get_assignment(user_id: int | str, state: FSMContext):
    assignment_data: dict[str, Any] = await state.get_data()
    step: int = assignment_data['step'] + 1
    
    try:
        assignment_id: int = int(assignment_data['assignments_ids'].split('_')[step])
    except:
        assignment_id = None
        
    if assignment_id:
        assignment: Assignment = await Assignment.objects.aget(id=assignment_id)

        await state.update_data(
            step=step,
            current_question_id=assignment.pk,
            current_question_type=assignment.question_type,
        )   
  
        if assignment.question_type == 'select_one':
            options: list[str] = [
                assignment.choice_1, 
                assignment.choice_2,
                assignment.choice_3,
                assignment.correct_answer
            ]
            shuffle(options)
            correct_option_id: int = options.index(assignment.correct_answer)
            poll_message: Message = await bot.send_poll(
                chat_id=user_id,
                question=f'Задание {step+1} из {assignment_data["number_of_assignments"]}\n\n' + assignment.question,
                options=options,
                type='quiz',
                correct_option_id=correct_option_id,
                is_anonymous=False,
            )
            await state.update_data(
                correct_option_id=correct_option_id, 
                poll_message_id=poll_message.message_id
            )
        elif assignment.question_type == 'short_reply':  
            await bot.send_message(
                chat_id=user_id,
                text=f'Задание {step + 1} из {assignment_data["number_of_assignments"]}\n\n' + assignment.question,
            )
            await state.update_data(correct_answer=assignment.correct_answer)
            
        if assignment.image:
            image_message = await bot.send_photo(
                chat_id=user_id,
                photo=FSInputFile('media/' + str(assignment.image))
            )
            await state.update_data(image_message_id=image_message.message_id)
             
        await state.set_state(TakeExam.get_result)
    else:
        result = await Results.objects.filter(
            category__id=assignment_data['category_id'], 
            user__user_id=user_id,
            status=True
        ).acount()
        all_assignments = await Assignment.objects.filter(
            category__id=assignment_data['category_id']
        ).acount()
        category_name = await Category.objects.aget(
            id=assignment_data['category_id']
        )
        await bot.send_message(
            chat_id=user_id,
            text=BotVocabulary.message_no_more_questions(
                result=result, 
                numbers=all_assignments, 
                category_name=category_name
            ),
            reply_markup=make_restart_keyboard()
        )
        await state.set_state(TakeExam.no_more_questions)


@router.poll_answer(StateFilter(TakeExam.get_result))
async def get_result_assignment_poll(poll_answer: PollAnswer, state: FSMContext):
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


@router.callback_query(StateFilter(TakeExam.no_more_questions), F.data=='restart')
async def restart_exam(callback: CallbackQuery, state: FSMContext):

    assignment_data: dict[str, Any] = await state.get_data()
    await Results.objects.filter(
        user__user_id=callback.from_user.id,
        category__id=assignment_data['category_id']
    ).adelete()
    
    assignments_ids = await get_assignments_ids(
        callback.from_user.id, 
        assignment_data['category_id']
    )
    number_of_assignments: int = len(assignments_ids.split('_'))
    
    await state.update_data(
        step=-1, 
        assignments_ids=assignments_ids, 
        number_of_assignments=number_of_assignments
    )
    await state.set_state(TakeExam.get_question)
    await get_assignment(callback.from_user.id, state)
