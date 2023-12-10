from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    #await state.clear()
    await message.answer(
        text="Привет-привет!",
        #reply_markup=ReplyKeyboardRemove()
    )