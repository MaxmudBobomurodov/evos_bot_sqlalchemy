from aiogram.fsm.state import State, StatesGroup


class CategoryAdd(StatesGroup):
    name_uz = State()
    name_ru = State()
    name_en = State()



class ProductAdd(StatesGroup):
    name_uz = State()
    name_ru = State()
    name_en = State()

    about_uz = State()
    about_ru = State()
    about_en = State()

    price = State()
    image = State()
    category_id = State()
