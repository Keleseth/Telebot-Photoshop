from aiogram.fsm.state import StatesGroup, State


class WhitelistState(StatesGroup):
    waiting_for_id_to_search = State()
    waiting_for_id_to_remove = State()
    waiting_for_id_to_add = State()