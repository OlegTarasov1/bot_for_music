from aiogram.filters.callback_data import CallbackData


class CountriesTopsCallback(
    CallbackData,
    prefix = "c"
):
    action: str = "get"
    offset: int = 0
    limit: int = 10
    
    limit_pl: int = 10
    offset_pl: int = 0
    
    track_id: int | None = None 
    country: str | None = None
    pl_id: int | None = None