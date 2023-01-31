from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    admin_mode_state = State()
