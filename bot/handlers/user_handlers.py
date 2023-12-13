from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from ..filters.is_admin import IsAdmin
from ..models import User
from ..keyboards.keyboards import game_kb, yes_no_kb
from ..services.services import get_bot_choice, get_winner
from ..services.vocabulary import BotVocabulary

router = Router()


@router.message(Command(commands=['start']))
async def start_command(message: Message):
    if message.from_user is None:
        return
    
    user, created = await User.objects.aget_or_create(
        user_id=message.from_user.id,
    )
    
    if created:
        await User.objects.filter(user_id=message.from_user.id).aupdate(
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
        
    await message.answer(text=await BotVocabulary.start(), parse_mode=ParseMode.MARKDOWN_V2)
    
    