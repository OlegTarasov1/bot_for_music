from aiogram.filters.callback_data import CallbackData


class GenresTopsCallback(
    CallbackData,
    prefix = "top_genres_"
):
    action: str = "get"
    offset: int = 0
    limit: int  = 9

    track_id: int | None = None    
    genre: str | None = None
