from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from .exam_handlers import get_assignment
from ..db_methods import get_assignments_ids, get_random_assignments_ids
from ..models import User
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
     
    await message.answer(
        text=BotVocabulary.command_menu,
        reply_markup=await make_menu_keyboard(message.from_user.id)
    )


@router.callback_query(CategoryCallbackFactory.filter())
async def get_category_assignments(callback: CallbackQuery, callback_data: CategoryCallbackFactory, state: FSMContext):
    """
    Обработчик нажатия на инлайн-кнопку с названием категории заданий.
    - Вызывает функцию get_assignments_ids() для получения строки с id вопросов
    выбранной категории для конкретного пользователя.
    - Вызывает функцию get_assignment() для получения задания.
    """
    await state.clear()
    
    assignments_ids: str = await get_assignments_ids(
        callback.from_user.id, 
        callback_data.category_id
    )
    number_of_assignments: int = len(assignments_ids.split('_'))
    
    await state.update_data(
        step=-1, # шаг
        category_id=callback_data.category_id, # id категории
        assignments_ids=assignments_ids, # строка с id всех заданий
        number_of_assignments=number_of_assignments, # количество заданий
    )
    await state.set_state(TakeExam.get_question)
    
    await get_assignment(callback.from_user.id, state)
    

@router.callback_query(F.data=='random')
async def get_random_assignments(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия на инлайн-кнопку "Случайно".
    - Вызывает функцию get_random_assignments_ids() для получения случайных 
    десяти (или меньше) id заданий.
    - Вызывает функцию get_assignment() для получения задания.
    """
    state.clear()
    
    assignments_ids: str = await get_random_assignments_ids()
    number_of_assignments: int = len(assignments_ids.split('_'))
    
    await state.update_data(
        step=-1, 
        category_id=None,
        assignments_ids=assignments_ids,
        number_of_assignments=number_of_assignments,
    )
    await state.set_state(TakeExam.get_question)
    
    await get_assignment(callback.from_user.id, state)

@router.callback_query(StateFilter(TakeExam.no_more_questions), F.data=='back_to_menu')
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия инлайн-кнопки "Вернуться в меню выбора" присылает 
    сообщение с текстом команды /menu и её инлайн-клавиатурой.
    """
    await state.clear()
    
    await callback.message.answer(
        text=BotVocabulary.command_menu,
        reply_markup=await make_menu_keyboard(callback.from_user.id)
    )
    
