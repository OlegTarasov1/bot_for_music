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

    message_text = "Введите текст, который вы хотите отправить пользователям.\n"
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
    text = msg.text.strip().lower()
    if text == "отмена":
        state.clear()
        await msg.answer("Ввод отменён")
    else:
        text = text.capitalize()
        await state.update_data(text = text)
        await state.set_state(SpamFSM.reply_markup)

        man_text = "Если хотите добавить ссылку пропишите текст для ссылки и саму ссылку через знак: \"|\" (если несколько, то через запятую)"
        man_text += "\n\n\nПример:\n\n"
        man_text += "текст для ссылки | https://...<сама ссылка>,\n"
        man_text += "текст для ссылки | https://...<сама ссылка>"
        await msg.answer(
            text = man_text,
            reply_markup = example_kb
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
            await msg.answer(
                text = data.get("text"),
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
        except:
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

            if markup_text:
                markup_lists = []

                markup_text = markup_text.split(",")                
                logging.warning(f"mk text: {markup_text}")
                logging.warning(f"msg_text: {msg_text}")

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
        

