from aiogram.fsm.state import StatesGroup, State


class LinkState(StatesGroup):
    waiting_for_token = State()


class NewNoteState(StatesGroup):
    title = State()
    content = State()
    tags = State()