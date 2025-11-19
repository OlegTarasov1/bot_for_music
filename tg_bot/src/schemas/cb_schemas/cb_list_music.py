from aiogram.filters.callback_data import CallbackData


class MusicCallback(CallbackData, prefix = "list_music", sep = "::"):
    action: str = "get"
    offset: int = 0
    limit: int = 10
