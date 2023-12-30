from aiogram.fsm.state import State, StatesGroup


class TakeExam(StatesGroup):
    start_exam = State()
    get_question = State()
    get_result = State()
    next_question = State()
    no_more_questions = State()