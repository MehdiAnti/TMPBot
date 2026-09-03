import requests

from config import BOT_TOKEN


API_URL = (
    f"https://api.telegram.org/bot{BOT_TOKEN}"
)

TIMEOUT = 15


def request(method, data=None):
    try:
        response = requests.post(
            f"{API_URL}/{method}",
            json=data or {},
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("ok"):
            print(
                f"Telegram API returned error: "
                f"{result}"
            )

            return None

        return result.get("result")

    except requests.RequestException as error:
        print(
            f"Telegram API error: {error}"
        )

        return None


def send_message(
    chat_id,
    text,
    reply_markup=None,
):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    if reply_markup is not None:
        data["reply_markup"] = reply_markup

    return request(
        "sendMessage",
        data,
    )


def edit_message(
    chat_id,
    message_id,
    text,
    reply_markup=None,
):
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
    }

    if reply_markup is not None:
        data["reply_markup"] = reply_markup

    return request(
        "editMessageText",
        data,
    )


def answer_callback(
    callback_query_id,
    text=None,
):
    data = {
        "callback_query_id": callback_query_id,
    }

    if text:
        data["text"] = text

    return request(
        "answerCallbackQuery",
        data,
    )


def set_webhook(url):
    return request(
        "setWebhook",
        {
            "url": url,
        },
    )
