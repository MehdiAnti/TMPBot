from telegram.api import (
    answer_callback,
    edit_message,
)

from telegram.keyboards import (
    events_keyboard,
    events_list_keyboard,
    event_detail_keyboard,
)

from truckersmp.api import get_events

from formatters.events import (
    format_events,
    format_event,
)


EVENT_CATEGORIES = (
    "featured",
    "today",
)

EVENTS_PER_PAGE = 5


def _get_category_events(
    events_data,
    category,
):
    if events_data is None:
        return None

    response = events_data.get(
        "response",
        {},
    )

    return response.get(
        category,
        [],
    )


def handle_events_callback(
    callback_id,
    chat_id,
    message_id,
    data,
):
    # Events overview
    if data in (
        "events",
        "events_refresh",
    ):
        answer_callback(
            callback_id,
            "Loading events...",
        )

        events_data = get_events()

        edit_message(
            chat_id,
            message_id,
            format_events(
                events_data
            ),
            events_keyboard(),
        )

        return True

    # Category
    if data.startswith(
        "events_category_"
    ):
        category = data.replace(
            "events_category_",
            "",
            1,
        )

        if category not in EVENT_CATEGORIES:
            answer_callback(
                callback_id,
                "Unknown event category.",
            )

            return True

        answer_callback(
            callback_id,
            "Loading events...",
        )

        events_data = get_events()

        if events_data is None:
            edit_message(
                chat_id,
                message_id,
                format_events(None),
                events_keyboard(),
            )

            return True

        events = _get_category_events(
            events_data,
            category,
        )

        if not events:
            edit_message(
                chat_id,
                message_id,
                (
                    f"📅 <b>{category.title()} Events</b>\n"
                    "━━━━━━━━━━━━━━━━\n\n"
                    "No events found."
                ),
                events_keyboard(),
            )

            return True

        edit_message(
            chat_id,
            message_id,
            (
                f"📅 <b>{category.title()} Events</b>\n"
                "━━━━━━━━━━━━━━━━\n\n"
                f"Found <b>{len(events)}</b> events.\n\n"
                "Select an event below:"
            ),
            events_list_keyboard(
                category,
                events,
                0,
                EVENTS_PER_PAGE,
            ),
        )

        return True

    # Pagination
    if data.startswith(
        "events_page_"
    ):
        parts = data.split(
            "_",
            3,
        )

        if len(parts) != 4:
            answer_callback(
                callback_id,
                "Invalid page.",
            )

            return True

        category = parts[2]

        try:
            page = int(parts[3])
        except ValueError:
            answer_callback(
                callback_id,
                "Invalid page.",
            )

            return True

        if category not in EVENT_CATEGORIES:
            answer_callback(
                callback_id,
                "Unknown event category.",
            )

            return True

        answer_callback(
            callback_id,
            "Loading events...",
        )

        events_data = get_events()

        if events_data is None:
            answer_callback(
                callback_id,
                "TruckersMP API unavailable.",
            )

            return True

        events = _get_category_events(
            events_data,
            category,
        )

        if not events:
            answer_callback(
                callback_id,
                "No events found.",
            )

            return True

        total_pages = (
            len(events)
            + EVENTS_PER_PAGE
            - 1
        ) // EVENTS_PER_PAGE

        if page < 0 or page >= total_pages:
            answer_callback(
                callback_id,
                "Invalid page.",
            )

            return True

        edit_message(
            chat_id,
            message_id,
            (
                f"📅 <b>{category.title()} Events</b>\n"
                "━━━━━━━━━━━━━━━━\n\n"
                f"Found <b>{len(events)}</b> events.\n\n"
                "Select an event below:"
            ),
            events_list_keyboard(
                category,
                events,
                page,
                EVENTS_PER_PAGE,
            ),
        )

        return True

    # Event details
    if data.startswith(
        "event_detail_"
    ):
        parts = data.split(
            "_",
            3,
        )

        if len(parts) != 4:
            answer_callback(
                callback_id,
                "Invalid event.",
            )

            return True

        category = parts[2]
        event_id = parts[3]

        if category not in EVENT_CATEGORIES:
            answer_callback(
                callback_id,
                "Unknown event category.",
            )

            return True

        answer_callback(
            callback_id,
            "Loading event...",
        )

        events_data = get_events()

        if events_data is None:
            answer_callback(
                callback_id,
                "TruckersMP API unavailable.",
            )

            return True

        events = _get_category_events(
            events_data,
            category,
        )

        event = next(
            (
                item
                for item in events
                if str(
                    item.get("id")
                ) == event_id
            ),
            None,
        )

        if event is None:
            answer_callback(
                callback_id,
                "Event not found.",
            )

            return True

        event_index = events.index(
            event
        )

        page = (
            event_index
            // EVENTS_PER_PAGE
        )

        edit_message(
            chat_id,
            message_id,
            format_event(
                event,
                event_index,
                len(events),
            ),
            event_detail_keyboard(
                category,
                page,
                event,
            ),
        )

        return True

    return False
