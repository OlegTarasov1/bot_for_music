from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_top_genres import GenresTopsCallback
import logging


async def get_kb_for_tops_by_genres(
    tags: list[str],
    offset: int = 0,
    limit: int = 9    
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    start = offset * limit
    finish = offset * limit + limit

    btns = []
    logging.warning("prior for loop")
    for i, value in enumerate(tags[start:finish]):
        btns.append(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value}",
                callback_data = GenresTopsCallback(
                    action = "retreive",
                    genre = f"top_{value.replace(' ', '_')}"
                ).pack()
            )
        )
    logging.warning("after for loop")
    kb.add(*btns)
    kb.adjust(3)

    nav_btns = []
    if start > 0:
        nav_btns.append(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = GenresTopsCallback(
                    offset = offset - 1
                ).pack()
            )
        ) 
    if finish < len(tags):
        nav_btns.append(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = GenresTopsCallback(
                    offset = offset + 1 
                ).pack() 
            )
        )

    kb.row(*nav_btns)

    kb.row(
        InlineKeyboardButton(
            text = "меню",
            callback_data = "menu"
        )
    )

    return kb.as_markup()



async def kb_track_retreival(
    limit: int,
    offset: int,
    track_id: int
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(
        *[
            InlineKeyboardButton(
                text = "Скачать",
                callback_data = GenresTopsCallback(
                    action = "download",
                    limit = limit,
                    track_id = track_id,
                    offset = offset
                ).pack()
            ),
            InlineKeyboardButton(
                text = "Назад",
                callback_data = GenresTopsCallback(
                    action = "retreive",
                    limit = limit,
                    offset = offset
                ).pack()
            ),
            InlineKeyboardButton(
                text = "Меню",
                callback_data = "menu"
            )
        ]
    )

    return kb.as_markup()







