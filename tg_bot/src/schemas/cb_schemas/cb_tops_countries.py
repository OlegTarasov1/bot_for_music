from aiogram.filters.callback_data import CallbackData


class CountriesTopsCallback(
    CallbackData,
    prefix = "c"
):
    action: str = "get"
    offset: int = 0
    limit: int = 10
    
    country: str | None
