from telegram.api import answer_callback

from handlers.callbacks.main import (
    handle_main_callback,
)

from handlers.callbacks.events import (
    handle_events_callback,
)

from handlers.callbacks.rules import (
    handle_rules_callback,
)


def handle_callback(callback):
    callback_id = callback["id"]
    data = callback.get("data", "")

    message = callback.get("message")

    if not message:
        answer_callback(
            callback_id,
            "Message unavailable.",
        )

        return

    chat_id = message["chat"]["id"]
    message_id = message["message_id"]

    if handle_main_callback(
        callback_id,
        chat_id,
        message_id,
        data,
    ):
        return

    if handle_events_callback(
        callback_id,
        chat_id,
        message_id,
        data,
    ):
        return

    if handle_rules_callback(
        callback_id,
        chat_id,
        message_id,
        data,
    ):
        return

    answer_callback(
        callback_id,
        "Unknown action.",
    )
