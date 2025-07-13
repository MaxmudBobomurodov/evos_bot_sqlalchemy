from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    language = State()
    phone_number = State()
    name = State()
    location = State()



class Feedback(StatesGroup):
    feedback = State()

class LocationState(StatesGroup):
    location = State()