from aiogram.fsm.state import State, StatesGroup


class TakeExam(StatesGroup):
    next_question = State()
    get_result = State()
    no_more_questions = State()