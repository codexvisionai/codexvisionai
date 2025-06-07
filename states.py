from aiogram.fsm.state import State, StatesGroup

class TestStates(StatesGroup):
    waiting_for_payment = State()
    choosing_direction = State()
    choosing_test = State()
    waiting_answers = State()
