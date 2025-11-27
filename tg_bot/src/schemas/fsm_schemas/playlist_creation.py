from aiogram.fsm.state import StatesGroup, State


class PlaylistCreation(StatesGroup):
    title = State()