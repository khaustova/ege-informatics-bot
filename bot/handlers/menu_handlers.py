from typing import Any
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from .exam_handlers import get_assignment, get_random_assignment
from ..models import Assignment, Results, User
from ..keyboards.factories import CategoryCallbackFactory
from ..keyboards.menu_keyboards import make_menu_keyboard
from ..states.take_exam import TakeExam
from ..services.vocabulary import BotVocabulary

router = Router()


@router.message(Command(commands=['start']))
async def start_command(message: Message, state: FSMContext):
    """
    Обработчик команды /start сохраняет информацию о новом пользователе и
    выводит инлайн-клавиатуру с меню выбора заданий.
    """
    await state.clear()
    
    user, created = await User.objects.aget_or_create(
        user_id=message.from_user.id,
    )
    if created:
        await user.objects.aupdate(
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
        
    await message.answer(
        text=BotVocabulary.command_start,
        reply_markup=await make_menu_keyboard(message.from_user.id)
    )
    
    
@router.message(Command(commands=['menu']))
async def menu_command(message: Message, state: FSMContext):
    """
    Обработчик команды /menu выводит  инлайн-клавитауру с меню выбора заданий.
    """
    await state.clear()
    await state.set_state(TakeExam.start_exam)
    
    await message.answer(
        text=BotVocabulary.command_menu,
        reply_markup=await make_menu_keyboard(message.from_user.id)
    )
    



@router.callback_query(StateFilter(TakeExam.start_exam), CategoryCallbackFactory.filter())
async def get_category_assignments(
    callback: CallbackQuery, 
    callback_data: CategoryCallbackFactory, 
    state: FSMContext
):
    """
    Обработчик нажатия на инлайн-кнопку с названием категории заданий определяет
    количество заданий в категории, количество решенных заданий и, в соответствии
    с этим, текующий шаг, после чего вызывает функцию получения задания.
    """
    #await state.clear()
    
    number_of_assignments: int = await Assignment.objects.filter(
        category=callback_data.category_id
    ).acount()
    done: int = await Results.objects.filter(
        user__user_id=callback.from_user.id, 
        category__id=callback_data.category_id
    ).acount()

    step: int = done - 1 if done else -1

    await state.update_data(
        step=step,
        category_id=callback_data.category_id,
        number_of_assignments=number_of_assignments
    )
    await state.set_state(TakeExam.get_question)
    
    await get_assignment(callback.from_user.id, state)
    
    
    
@router.callback_query(StateFilter(TakeExam.start_exam), F.data=='random')
async def random_mode(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия на инлайн-кнопку с выбором режима случайных заданий.
    """
    #await state.clear()
    await state.update_data(random=True)
    await state.set_state(TakeExam.get_question)
    
    await get_random_assignment(callback.from_user.id, state)
    

@router.callback_query(F.data=='random')
async def get_random_assignments(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия на инлайн-кнопку "Случайно" вызывает функцию 
    для получения случайных десяти (или меньше) заданий и функцию получения 
    задания.
    """
    state.clear()
    
    await state.update_data(
        step=-1, 
        category_id=None,
    )
    await state.set_state(TakeExam.get_question)
    
    await get_assignment(callback.from_user.id, state)

@router.callback_query(StateFilter(TakeExam.no_more_questions), F.data=='back_to_menu')
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия инлайн-кнопки возвращения в меню выбора задания присылает 
    сообщение с текстом команды /menu и её инлайн-клавиатурой.
    """
    await state.clear()
    await state.set_state(TakeExam.start_exam)
    
    await callback.message.answer(
        text=BotVocabulary.command_menu,
        reply_markup=await make_menu_keyboard(callback.from_user.id)
    )
    

@router.callback_query(StateFilter(TakeExam.no_more_questions), F.data=='restart')
async def restart_exam(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия инлайн-кнопки перезапуска заданий в разделе удаляет 
    весь текущий прогресс пользователя по разделу и вызывает функцию получения
    задания.
    """
    assignment_data: dict[str, Any] = await state.get_data()
    await Results.objects.filter(
        user__user_id=callback.from_user.id,
        category__id=assignment_data['category_id']
    ).adelete()
    
    number_of_assignments: int = await Assignment.objects.filter(
        category=assignment_data['category_id']
    ).acount()

    await state.update_data(
        step=-1, 
        number_of_assignments=number_of_assignments
    )
    await state.set_state(TakeExam.get_question)
    await get_assignment(callback.from_user.id, state)