from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from ..filters.is_admin import IsAdmin
from ..models import User

router = Router()

  
@router.message(Command(commands=['admin']), IsAdmin())
async def admin_command(message: Message):
    await message.answer(text='Админ?')