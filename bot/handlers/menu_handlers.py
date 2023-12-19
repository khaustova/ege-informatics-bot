from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from .exam_handlers import create_exam
from ..main import dp
from ..models import User
from ..states.take_exam import TakeExam
from ..db_methods import get_categories, get_subcategories, get_questions
from ..keyboards.factories import CategoryCallbackFactory, SubcategoryCallbackFactory
from ..keyboards.main_menu_keyboards import (
    make_menu_keyboard, 
    make_subcategory_keyboard
)

router = Router()


@router.message(Command(commands=['start']))
async def start_command(message: Message):
    user, created = await User.objects.aget_or_create(
        user_id=message.from_user.id,
    )
    if created:
        await user.objects.aupdate(
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
        
    categories = await get_categories() 
    await message.answer(
        text='Привет! Это тренажёр для подготовки к ЕГЭ по информатике! Выбери категорию.',
        reply_markup=make_menu_keyboard(categories)
    )


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
    )


@dp.callback_query(StateFilter(default_state), CategoryCallbackFactory.filter())
async def get_category(callback: CallbackQuery, callback_data: CategoryCallbackFactory, state: FSMContext):
    subcategories = await get_subcategories(callback_data.category_id)
    await callback.message.answer(
        text='Теперь выбери подкатегорию.',
        reply_markup=make_subcategory_keyboard(subcategories)
    )
    await callback.answer()
    await state.set_state(TakeExam.start_exam)
    
    
@dp.callback_query(StateFilter(TakeExam.start_exam), SubcategoryCallbackFactory.filter())
async def get_subcategory(callback: CallbackQuery, callback_data: SubcategoryCallbackFactory, state: FSMContext):
    questions = await get_questions(callback.from_user.id, callback_data.subcategory_id)
    await state.set_state(TakeExam.next_question)
    await create_exam(callback.message.chat.id, callback.from_user.id, questions, state)

