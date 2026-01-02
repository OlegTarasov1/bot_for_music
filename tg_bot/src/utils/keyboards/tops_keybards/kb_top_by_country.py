from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas.cb_schemas.cb_tops_countries import CountriesTopsCallback



async def list_top_for_country_kb(
    country_name: str,
    top_countries_json: dict,
    limit: int = 10,
    offset: int = 0
):
    kb = InlineKeyboardBuilder()

    start = offset * limit
    finish = start + limit

    for i, value in enumerate(top_countries_json[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.get('title', 'title')}",
                callback_data = CountriesTopsCallback(
                    action = "retreive",
                    country = country_name,
                    track_id = value.get("id", None),
                    limit = limit,
                    offset = offset
                ).pack()
            )
        )

    kb.adjust(2)

    nav = []

    if start > 0:
        nav.append(
            InlineKeyboardButton(
                text = "◀️ Назад",
                callback_data = CountriesTopsCallback(
                    action = "get_c_top",
                    limit=limit,
                    offset=offset - 1,
                    country=country_name
                ).pack()
            )
        )

    if finish < len(top_countries_json):
        nav.append(
            InlineKeyboardButton(
                text = "Вперёд ▶️",
                callback_data =  CountriesTopsCallback(
                    action = "get_c_top",
                    limit=limit,
                    offset=offset + 1,
                    country=country_name
                ).pack()
            )
        )

    kb.row(
        *nav
    )

    kb.row(
        InlineKeyboardButton(
            text = "Вернуться ↩️",
            callback_data = "tops_by_countries"
        )
    )

    kb.row(
        InlineKeyboardButton(
            text = "🔙 Назад",
            callback_data = "menu"
        )
    )

    return kb.as_markup()