from telegram.api import (
    answer_callback,
    edit_message,
)

from telegram.keyboards import (
    rules_keyboard,
    rule_section_keyboard,
)

from truckersmp.api import get_rules

from formatters.rules import (
    format_rules,
)

from utils.rules_parser import (
    get_rule_section,
    get_rule_title,
)


def _format_rule_page(
    pages,
    page,
):
    text = pages[page]

    if len(pages) > 1:
        text += (
            "\n\n━━━━━━━━━━━━━━━━\n"
            f"📄 Page "
            f"<b>{page + 1}/{len(pages)}</b>"
        )

    return text


def handle_rules_callback(
    callback_id,
    chat_id,
    message_id,
    data,
):
    # Rules overview
    if data in (
        "rules",
        "rules_refresh",
    ):
        answer_callback(
            callback_id,
            "Loading rules...",
        )

        rules_data = get_rules()

        edit_message(
            chat_id,
            message_id,
            format_rules(
                rules_data
            ),
            rules_keyboard(),
        )

        return True

    # Rule section
    if data.startswith(
        "rules_section_"
    ):
        section_id = data.replace(
            "rules_section_",
            "",
            1,
        )

        answer_callback(
            callback_id,
            "Loading rule section...",
        )

        rules_data = get_rules()

        if rules_data is None:
            edit_message(
                chat_id,
                message_id,
                (
                    "⚠️ <b>TruckersMP Rules</b>\n"
                    "━━━━━━━━━━━━━━━━\n\n"
                    "TruckersMP API unavailable.\n\n"
                    "Please try again later."
                ),
                rules_keyboard(),
            )

            return True

        rules = rules_data.get(
            "rules",
            "",
        )

        pages = get_rule_section(
            rules,
            section_id,
        )

        title = get_rule_title(
            section_id
        )

        if not pages:
            edit_message(
                chat_id,
                message_id,
                (
                    f"⚠️ <b>{title}</b>\n"
                    "━━━━━━━━━━━━━━━━\n\n"
                    "This rule section could not "
                    "be found."
                ),
                rules_keyboard(),
            )

            return True

        edit_message(
            chat_id,
            message_id,
            _format_rule_page(
                pages,
                0,
            ),
            rule_section_keyboard(
                section_id,
                0,
                len(pages),
            ),
        )

        return True

    # Rule pagination
    if data.startswith(
        "rules_page_"
    ):
        parts = data.split("_")

        if len(parts) != 4:
            answer_callback(
                callback_id,
                "Invalid page.",
            )

            return True

        section_id = parts[2]

        try:
            page = int(parts[3])
        except ValueError:
            answer_callback(
                callback_id,
                "Invalid page.",
            )

            return True

        answer_callback(
            callback_id,
            "Loading page...",
        )

        rules_data = get_rules()

        if rules_data is None:
            answer_callback(
                callback_id,
                "TruckersMP API unavailable.",
            )

            return True

        rules = rules_data.get(
            "rules",
            "",
        )

        pages = get_rule_section(
            rules,
            section_id,
        )

        if not pages:
            answer_callback(
                callback_id,
                "Rule section not found.",
            )

            return True

        if page < 0 or page >= len(pages):
            answer_callback(
                callback_id,
                "Invalid page.",
            )

            return True

        edit_message(
            chat_id,
            message_id,
            _format_rule_page(
                pages,
                page,
            ),
            rule_section_keyboard(
                section_id,
                page,
                len(pages),
            ),
        )

        return True

    return False
