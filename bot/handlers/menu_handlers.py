from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from .exam_handlers import create_exam
from ..main import dp
from ..models import User
from ..db_methods import get_categories, get_subcategories
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


@dp.callback_query(CategoryCallbackFactory.filter())
async def get_category(callback: CallbackQuery, callback_data: CategoryCallbackFactory):
    subcategories = await get_subcategories(callback_data.category_id)
    await callback.message.answer(
        text=callback_data.pack(),
        reply_markup=make_subcategory_keyboard(subcategories)
    )
    await callback.answer()
    
    
@dp.callback_query(SubcategoryCallbackFactory.filter())
async def get_subcategory(callback: CallbackQuery, callback_data: SubcategoryCallbackFactory):
    await create_exam(callback.message.chat.id, callback.from_user.id)
