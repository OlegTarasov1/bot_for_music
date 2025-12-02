from aiogram.filters.callback_data import CallbackData


class PlaylistCallback(
    CallbackData,
    prefix = "p"
):
    # действие, что обрабатывать, собственно
    action: str = "get"

    # данные для пагинации по плкйлистам
    offset: int = 0
    limit: int  = 6

    # данные для пагинации по трекам
    track_limit: int = 6
    track_offset: int = 0

    # метаданные, ради которых всё и затевалось
    playlist_id: int | None = None
    track_id: int | None = None