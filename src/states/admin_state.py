from aiogram.fsm.state import State, StatesGroup

class AdminState(StatesGroup):
    add_category = State()
    add_service = State()
    add_admin = State()