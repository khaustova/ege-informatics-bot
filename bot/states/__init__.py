from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class TakeQuiz(StatesGroup):
    next_question = State()