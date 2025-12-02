from aiogram.filters.callback_data import CallbackData


class TrackCallbacks(
    CallbackData,
    prefix = "t"
):
    action: str = "add"
    offset: int = 0
    limit: int = 10

    request: str
    track_id: int
    playlist_id: int
    