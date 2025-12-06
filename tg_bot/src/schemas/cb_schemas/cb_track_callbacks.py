from aiogram.filters.callback_data import CallbackData


class TrackCallbacks(
    CallbackData,
    prefix = "t"
):
    action: str = "add"
    offset: int = 0
    limit: int = 10

    request: str | None = None
    track_id: int | None = None
    playlist_id: int | None = None
    