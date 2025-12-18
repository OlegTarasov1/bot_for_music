from aiogram.fsm.state import StatesGroup, State


class SpamFSM(StatesGroup):
    text = State()
    media = State()
    reply_markup = State()
    verification = State()