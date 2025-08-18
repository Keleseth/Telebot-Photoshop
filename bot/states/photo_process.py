from aiogram.fsm.state import StatesGroup, State


class PhotoProcessState(StatesGroup):
    """
    State class for processing user's photo enhancement.

    Attributes:
        waiting_instructions: the state when a photo has been
        received and instructions are awaited.
    """

    waiting_instructions = State()
    awaiting_order = State()