from aiogram.fsm.state import State, StatesGroup


class TakeExam(StatesGroup):
    get_question = State()
    get_result = State()
    next_question = State()
    no_more_questions = State()