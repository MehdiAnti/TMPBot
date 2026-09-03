from telegram.api import (
    answer_callback,
    edit_message,
)

from telegram.keyboards import (
    main_keyboard,
    page_keyboard,
)

from truckersmp.api import (
    get_servers,
    get_game_time,
    get_version,
)

from formatters.main import (
    format_servers,
    format_status,
    format_game_time,
    format_version,
)


def handle_main_callback(
    callback_id,
    chat_id,
    message_id,
    data,
):
    if data == "main_menu":
        answer_callback(callback_id)

        edit_message(
            chat_id,
            message_id,
            (
                "🚛 <b>TruckersMP Status</b>\n"
                "━━━━━━━━━━━━━━━━\n\n"
                "Choose an option below:"
            ),
            main_keyboard(),
        )

        return True

    if data == "main_refresh":
        answer_callback(
            callback_id,
            "Refreshing...",
        )

        edit_message(
            chat_id,
            message_id,
            (
                "🚛 <b>TruckersMP Status</b>\n"
                "━━━━━━━━━━━━━━━━\n\n"
                "Choose an option below:"
            ),
            main_keyboard(),
        )

        return True

    if data in (
        "servers",
        "servers_refresh",
    ):
        answer_callback(
            callback_id,
            "Loading servers...",
        )

        servers = get_servers()

        edit_message(
            chat_id,
            message_id,
            format_servers(servers),
            page_keyboard(
                "servers_refresh"
            ),
        )

        return True

    if data in (
        "status",
        "status_refresh",
    ):
        answer_callback(
            callback_id,
            "Updating status...",
        )

        servers = get_servers()

        edit_message(
            chat_id,
            message_id,
            format_status(servers),
            page_keyboard(
                "status_refresh"
            ),
        )

        return True

    if data in (
        "game_time",
        "game_time_refresh",
    ):
        answer_callback(
            callback_id,
            "Loading game time...",
        )

        game_time = get_game_time()

        edit_message(
            chat_id,
            message_id,
            format_game_time(
                game_time
            ),
            page_keyboard(
                "game_time_refresh"
            ),
        )

        return True

    if data in (
        "version",
        "version_refresh",
    ):
        answer_callback(
            callback_id,
            "Loading version...",
        )

        version = get_version()

        edit_message(
            chat_id,
            message_id,
            format_version(version),
            page_keyboard(
                "version_refresh"
            ),
        )

        return True

    return False
