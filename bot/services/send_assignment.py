from random import shuffle
from typing import Any
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from ..main import bot
from ..models import Assignment, Category, Results
from ..keyboards.exam_keyboards import make_restart_keyboard
from ..states.take_exam import TakeExam
from ..services.vocabulary import BotVocabulary


async def send_assignment(
    user_id: int | str,
    assignment: Assignment, 
    state: FSMContext
):
    """
    Отправляет сообщение с заданием в зависимости от его типа, а также, 
    при наличии, изображение.
    """
    assignment_data: dict[str, Any] = await state.get_data()
    step: int = assignment_data.get('step', -1) + 1

    await state.update_data(
        step=step,
        current_question_id=assignment.pk,
        current_question_type=assignment.question_type,
    )   
         
    if assignment.image:
        await bot.send_photo(
            chat_id=user_id,
            photo=FSInputFile('media/' + str(assignment.image))
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
        
        if assignment_data.get('random'):
            question_text = assignment.question
        else:
            question_text = f'Задание {step+1} из {assignment_data.get("number_of_assignments")}\n\n'
        
        poll_message: Message = await bot.send_poll(
            chat_id=user_id,
            question=question_text,
            options=options,
            type='quiz',
            correct_option_id=correct_option_id,
            is_anonymous=False
        )
        await state.update_data(
            correct_option_id=correct_option_id, 
            poll_message_id=poll_message.message_id
        )
    elif assignment.question_type == 'short_reply':  
        if assignment_data.get('random'):
            question_text = assignment.question
        else:
            question_text = f'<b>Задание {step+1} из {assignment_data.get("number_of_assignments")}</b>\n\n' \
                + assignment.question
        
        await bot.send_message(
            chat_id=user_id,
            text=question_text,
            parse_mode=ParseMode.HTML
        )
        await state.update_data(correct_answer=assignment.correct_answer)
            
    await state.set_state(TakeExam.get_result)


async def end_of_assignment(user_id: int | str, category_id: int, state: FSMContext):
    """
    Отправляет сообщение с уведомлением о том, что в выбранном разделе больше 
    нет заданий, и инлайн-клавиатуру с возможностью выбора сброса прогресса 
    по разделу или возвращения в главное меню.
    """
    result = await Results.objects.filter(
        category__id=category_id, 
        user__user_id=user_id,
        status=True
    ).acount()
    all_assignments = await Assignment.objects.filter(
        category__id=category_id
    ).acount()
    category_name = await Category.objects.aget(id=category_id)
    
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
