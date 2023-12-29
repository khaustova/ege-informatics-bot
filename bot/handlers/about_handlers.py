from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from ..services.vocabulary import BotVocabulary

router = Router()

  
@router.message(Command(commands=['about']))
async def admin_command(message: Message):
    """
    Обработчик команды /about отправляет сообщение с информацией о боте.
    """
    await message.answer(text=f'{BotVocabulary.command_about}')