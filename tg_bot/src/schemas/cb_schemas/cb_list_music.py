from aiogram.filters.callback_data import CallbackData


class MusicCallback(CallbackData, prefix = "l"):
    action: str = "get"
    offset: int = 0
    limit: int = 10
    
    request: str
    track_id: int | None = None
