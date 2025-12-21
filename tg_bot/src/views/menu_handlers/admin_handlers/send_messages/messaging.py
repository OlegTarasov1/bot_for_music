from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from schemas.fsm_schemas.spam_fsm import SpamFSM
from utils.sql_requests.user_requests import UsersRequestsSQL
from aiogram.fsm.context import FSMContext
from utils.keyboards.menus.spam_kbs.check_correctness import is_correct_kb, example_kb, kb_with_links, answer_kb
from utils.sql_requests.user_requests import UsersRequestsSQL
from utils.extra_funcs.spam import start_spamming
import logging


messaging_router = Router()


# Начало попытки отправить массовое сообщение всем пользователям.
# По факту: сбор текста этого сообщения.

@messaging_router.callback_query(F.data == "send_messages")
async def spamming_start(
    cb: CallbackQuery,
    state: FSMContext
): 
    user = await UsersRequestsSQL.get_user_by_id(
        tg_id = cb.from_user.id
    )

    message_text = "Введите текст (медиа), который вы хотите отправить пользователям.\n"
    message_text += "Введите: \"Отмена\", чтобы остановить ввод.\n"
    message_text += "(далее вы сможете установить ссылки)"

    if user.is_admin:
        await state.set_state(SpamFSM.text)

        await cb.message.answer(
            text = message_text
        )


# Получение текста сообщения и проверка его корректности.

@messaging_router.message(SpamFSM.text)
async def get_text_for_spam(
    msg: Message,
    state: FSMContext
):
    text = msg.text.strip().lower() if msg.text else msg.caption.strip().lower()
    if text == "отмена":
        await state.clear()
        await msg.answer("Ввод отменён")
    else:
        text = msg.text.capitalize() if msg.text else msg.caption.capitalize()
        
        logging.warning(msg.entities)

        await state.update_data(text = text)
        await state.update_data(entities = msg.entities if msg.entities else msg.caption_entities)

        await state.set_state(SpamFSM.reply_markup)

        message_text = "Если хотите добавить ссылку пропишите текст для ссылки и саму ссылку через знак: \"|\" (если несколько, то через запятую)"
        message_text += "\n\n\nПример:\n\n"
        message_text += "текст для ссылки | https://...<сама ссылка>,\n"
        message_text += "текст для ссылки | https://...<сама ссылка>"

        if msg.photo:
            file_id = f"photo_{msg.photo[-1].file_id}"
            await state.set_state(SpamFSM.reply_markup)
            await state.update_data(media = file_id)

        elif msg.animation:
            file_id = f"animation_{msg.animation.file_id}"
            await state.set_state(SpamFSM.reply_markup)
            await state.update_data(media = file_id)

        elif msg.video:
            file_id = f"video_{msg.video.file_id}"
            await state.set_state(SpamFSM.reply_markup)
            await state.update_data(media = file_id)

        await msg.answer(
            text = message_text
            # reply_markup = example_kb
        )


# Получение клавиатуры из сообщения
# Отправка тестового сообщения
@messaging_router.message(SpamFSM.reply_markup)
async def set_markup(
    msg: Message,
    state: FSMContext
):
    if msg.text.strip().lower() == "отмена":
        await state.clear()
        await msg.answer("Ввод отменён")

    elif msg.text.strip().lower() == "нет":
        await state.set_state(SpamFSM.verification)
        data = await state.get_data()

        if data.get("media", None):
            logging.warning(data.get("media")[:5])
            match data.get("media")[:5]:
                case "photo":
                    await msg.answer_photo(
                        caption_entities = data.get("entities"),
                        caption = data.get("text"),
                        photo = data.get("media", "").strip("photo_") if data.get("media") else None,
                    )
                case "video":
                    await msg.answer_video(
                        caption_entities = data.get("entities"),
                        caption = data.get("text"),
                        video = data.get("media", "").strip("video_") if data.get("media") else None
                    )
                case "anima":
                    await msg.answer_animation(
                        caption_entities = data.get("entities"),
                        caption = data.get("text"),
                        animation = data.get("media", "").strip("video_") if data.get("media") else None,
                        reply_markup = await kb_with_links(
                            markup_lists
                        )
                    )
                case _:
                    logging.error(data.get("media"))
                    await msg.answer(
                        text = "некорректные данные (media)"
                    )
        else:
            await msg.answer(
                entities = data.get("entities"),
                text = data.get("text")
            )

        await msg.answer(
            text = "всё корректно?",
            reply_markup = answer_kb
        )   

    elif len(msg.text.split("|")) > 0:
        markup_text = msg.text
        
        try:
            markup_text = markup_text.split(",")

            markup_lists = []
            for i in markup_text:
                start, finish, *_ = i.split("|")
                
                markup_lists.append(
                    (start.strip(), finish.strip())
                )

            data = await state.get_data()
            if data.get("media", None):
                logging.warning(data.get("media")[:5])
                match data.get("media")[:5]:
                    case "photo":
                        await msg.answer_photo(
                            caption = data.get("text"),
                            caption_entities = data.get("entities"),
                            photo = data.get("media").strip("photo_"),
                            reply_markup = await kb_with_links(
                                markup_lists
                            )
                        )
                    case "video":
                        await msg.answer_video(
                            caption = data.get("text"),
                            caption_entities = data.get("entities"),
                            video = data.get("media").strip("video_"),
                            reply_markup = await kb_with_links(
                                markup_lists
                            )
                        )
                    case "anima":
                        await msg.answer_animation(
                            caption = data.get("text"),
                            caption_entities = data.get("entities"),
                            animation = data.get("media").strip("video_"),
                            reply_markup = await kb_with_links(
                                markup_lists
                            )
                        )
                    case _:
                        logging.error(data.get("media"))
                        await msg.answer(
                            text = "некорректные данные (media)"
                        )

            else:
                await msg.answer(
                    text = data.get("text"),
                    entities = data.get("entities"),
                    reply_markup = await kb_with_links(
                        markup_lists
                    )
                )

            await msg.answer(
                text = "Всё верно?:",
                reply_markup = answer_kb
            )
            await state.update_data(reply_markup = msg.text)
            await state.set_state(SpamFSM.verification)

        except Exception as e:
            logging.error(e)
            await msg.answer("Введены не корректные данные")


# Обработка ответа о корректности сообщения для рассылки
# Сам факт рассылки
@messaging_router.message(SpamFSM.verification)
async def correctness_check(
    msg: Message,
    state: FSMContext
):
    match msg.text.strip().lower():

        case "да":
            data = await state.get_data()

            msg_text = str(data.get("text"))
            markup_text = str(data.get("reply_markup"))
            
            if markup_text != "None":
                logging.warning(f"markup text passed: {markup_text}")
                
                markup_lists = []

                markup_text = markup_text.split(",")                
                
                for i in markup_text:
                    start, finish, *_ = i.split("|")
                    
                    markup_lists.append(
                        (start.strip(), finish.strip())
                    )
            else:
                markup_lists = None

            users_list = await UsersRequestsSQL.get_all_users()

            for i in users_list:
                await start_spamming(
                    user = i,
                    message_text = msg_text,
                    media = data.get("media"),
                    entities = data.get("entities"),
                    markup = await kb_with_links(
                        markup_lists
                    ) if markup_lists else None
                )
            await state.clear()
            await msg.answer(
                text = "Сообщения отправлены."
            )

        case "нет":
            await state.set_state(SpamFSM.reply_markup)
            man_text = "Если хотите добавить ссылку пропишите текст для ссылки и саму ссылку через знак: \"|\" (если несколько, то через запятую)"
            man_text += "\n\n\nПример:\n\n"
            man_text += "текст для ссылки | https://...<сама ссылка>,\n"
            man_text += "текст для ссылки | https://...<сама ссылка>"
            await msg.answer(
                text = man_text,
                reply_markup = example_kb
            )

        case "отмена":
            await state.clear()
            await msg.answer("Ввод отменён")
        

