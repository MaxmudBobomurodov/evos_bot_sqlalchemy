from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    language = State()
    phone_number = State()
    name = State()



class Feedback(StatesGroup):
    feedback = State()