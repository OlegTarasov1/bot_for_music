from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_tops_countries import CountriesTopsCallback
from schemas.cb_schemas.cb_list_music import MusicCallback
from models import PlaylistsBase


async def kb_choose_pl(
    playlists: list[PlaylistsBase],
    country: str,
    track_id: str,
    limit: int = 10,
    offset: int = 0,
    limit_pl: int = 10,
    offset_pl: int = 0
):
    kb = InlineKeyboardBuilder()

    start = limit_pl * offset_pl
    finish = start + limit_pl

    for i, value in enumerate(playlists[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + 1 + i}. {value.title}",
                callback_data = CountriesTopsCallback(
                    action = "add_pl",
                    track_id = track_id,
                    limit = limit,
                    offset = offset,
                    pl_id = value.id,
                    country = country,
                    offset_pl = offset_pl,
                    limit_pl = limit_pl
                ).pack()
            )
        )

    kb.adjust(2)

    nav = []

    if start > 0:
        nav.append(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = CountriesTopsCallback(
                    action = "choose_pl",
                    track_id = track_id,
                    limit = limit,
                    country = country,
                    offset = offset,
                    offset_pl = offset_pl - 1,
                    limit_pl = limit_pl
                ).pack()
            )
        )

    if finish < len(playlists):
        nav.append(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = CountriesTopsCallback(
                    action = "choose_pl",
                    track_id = track_id,
                    country = country,
                    limit = limit,
                    offset = offset,
                    offset_pl = offset_pl + 1,
                    limit_pl = limit_pl
                ).pack()
            )
        )

    kb.row(*nav)

    kb.row(
        InlineKeyboardButton(
            text = "Вернуться",
            callback_data = CountriesTopsCallback(
                action = "retreive",
                track_id = track_id,
                limit = limit,
                country = country,
                offset = offset,
                offset_pl = offset_pl,
                limit_pl = limit_pl
            ).pack()
            
        )
    )

    kb.row(
        InlineKeyboardButton(
            text = "Меню",
            callback_data = "menu"
        )
    )

    return kb.as_markup()