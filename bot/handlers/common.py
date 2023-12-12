from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from ..models import User

router = Router()

@router.message(Command(commands=['start']))
async def start_command(message: Message):
    user, created = await User.objects.aget_or_create(
        user_id=message.from_user.id,
    )
    
    if created:
        await User.objects.filter(user_id=user.user_id).aupdate(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        
    start_text = 'Только что создан!' if created else 'Приветики!'
    
    await message.answer(
        text=start_text,
    )