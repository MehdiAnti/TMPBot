from telegram.api import send_message
from telegram.keyboards import main_keyboard

from formatters.main import welcome_message


def handle_message(message):
    text = message.get("text", "")
    chat_id = message["chat"]["id"]

    command = (
        text.split()[0].lower()
        if text
        else ""
    )

    if command in (
        "/start",
        "/help",
    ):
        send_message(
            chat_id,
            welcome_message(),
            reply_markup=main_keyboard(),
        )
