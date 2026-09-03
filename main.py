from flask import Flask, request

from config import (
    PORT,
    WEBHOOK_URL,
)

from telegram.api import set_webhook

from handlers.commands import (
    handle_message,
)

from handlers.callbacks import (
    handle_callback,
)


app = Flask(__name__)


@app.route(
    "/",
    methods=["GET"],
)
def index():
    return (
        "TruckersMP Status Bot is running!",
        200,
    )


@app.route(
    "/webhook",
    methods=["POST"],
)
def webhook():
    update = request.get_json(
        silent=True
    )

    if not update:
        return (
            "Invalid update",
            400,
        )

    if "message" in update:
        handle_message(
            update["message"]
        )

    elif "callback_query" in update:
        handle_callback(
            update["callback_query"]
        )

    return "OK", 200


def setup_webhook():
    webhook_url = (
        f"{WEBHOOK_URL}/webhook"
    )

    set_webhook(
        webhook_url
    )


if __name__ == "__main__":
    setup_webhook()

    app.run(
        host="0.0.0.0",
        port=PORT,
    )
