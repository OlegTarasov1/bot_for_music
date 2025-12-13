from aiogram.types import (
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder



is_correct_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "Всё корректно",
                callback_data = "shutter"
            ),
            InlineKeyboardButton(
                text = "Изменить",
                callback_data = "shutter"
            )
        ],
        [
            InlineKeyboardButton(
                text = "Меню",
                callback_data = "menu"
            )
        ]
    ]
)


example_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "текст для ссылки",
                callback_data = "shutter"
            )
        ],
        [
            InlineKeyboardButton(
                text = "текст для ссылки",
                callback_data = "shutter"
            )
        ]
    ]
)

async def kb_with_links(
    kb_data: list[tuple[str, str]]
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for i in kb_data:
        kb.add(
            InlineKeyboardButton(
                text = str(i[0]),
                url = str(i[1])
            )
        )

    kb.adjust(1)

    return kb.as_markup()

answer_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(
                text = "Да"
            ),
            KeyboardButton(
                text = "Нет"
            )
        ],
        [
            KeyboardButton(
                text = "Отмена"
            )
        ]
    ],
    resize_keyboard = True,
    one_time_keyboard = True
)