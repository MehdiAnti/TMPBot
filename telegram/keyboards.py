def button(
    text,
    callback_data=None,
    style="primary",
    url=None,
):
    result = {
        "text": text,
        "style": style,
    }

    if callback_data is not None:
        result["callback_data"] = callback_data

    if url is not None:
        result["url"] = url

    return result


def main_keyboard():
    return {
        "inline_keyboard": [
            [
                button(
                    "🖥 Servers",
                    "servers",
                ),
                button(
                    "🕐 Game Time",
                    "game_time",
                ),
            ],
            [
                button(
                    "🎮 Version",
                    "version",
                ),
                button(
                    "📅 Events",
                    "events",
                ),
            ],
            [
                button(
                    "📜 Rules",
                    "rules",
                ),
                button(
                    "📊 Status",
                    "status",
                    "success",
                ),
            ],
            [
                button(
                    "🔄 Refresh",
                    "main_refresh",
                    "success",
                ),
            ],
        ]
    }


def page_keyboard(refresh_callback):
    return {
        "inline_keyboard": [
            [
                button(
                    "🔄 Refresh",
                    refresh_callback,
                    "success",
                ),
            ],
            [
                button(
                    "↩️ Back",
                    "main_menu",
                    "primary",
                ),
            ],
        ]
    }


def rules_keyboard():
    return {
        "inline_keyboard": [
            [
                button(
                    "1️⃣ Service-wide",
                    "rules_section_1",
                ),
                button(
                    "2️⃣ Game Rules",
                    "rules_section_2",
                ),
            ],
            [
                button(
                    "3️⃣ Save Editing",
                    "rules_section_3",
                ),
                button(
                    "4️⃣ Forum Rules",
                    "rules_section_4",
                ),
            ],
            [
                button(
                    "5️⃣ Information",
                    "rules_section_5",
                ),
            ],
            [
                button(
                    "🌐 Official Rules",
                    url="https://truckersmp.com/rules",
                    style="success",
                ),
            ],
            [
                button(
                    "🔄 Refresh",
                    "rules_refresh",
                ),
                button(
                    "↩️ Back",
                    "main_menu",
                ),
            ],
        ]
    }


def rule_section_keyboard(
    section_id,
    page,
    total_pages,
):
    buttons = []

    navigation = []

    if page > 0:
        navigation.append(
            button(
                "◀️ Previous",
                f"rules_page_{section_id}_{page - 1}",
            )
        )

    if page < total_pages - 1:
        navigation.append(
            button(
                "Next ▶️",
                f"rules_page_{section_id}_{page + 1}",
            )
        )

    if navigation:
        buttons.append(navigation)

    buttons.append(
        [
            button(
                "📚 All Sections",
                "rules",
                "success",
            ),
        ]
    )

    buttons.append(
        [
            button(
                "↩️ Back",
                "main_menu",
            ),
        ]
    )

    return {
        "inline_keyboard": buttons
    }


def events_keyboard():
    return {
        "inline_keyboard": [
            [
                button(
                    "⭐ Featured",
                    "events_category_featured",
                ),
                button(
                    "📅 Today",
                    "events_category_today",
                    "success",
                ),
            ],
            [
                button(
                    "🔄 Refresh",
                    "events_refresh",
                    "success",
                ),
                button(
                    "↩️ Back",
                    "main_menu",
                    "primary",
                ),
            ],
        ]
    }


def events_list_keyboard(
    category,
    events,
    page,
    per_page=5,
):
    buttons = []

    start = page * per_page
    end = start + per_page

    page_events = events[start:end]

    for event in page_events:
        event_id = event.get("id")

        event_name = event.get(
            "name",
            "Unknown Event",
        )

        if len(event_name) > 35:
            event_name = (
                event_name[:32] + "..."
            )

        buttons.append(
            [
                button(
                    f"🚛 {event_name}",
                    (
                        f"event_detail_"
                        f"{category}_"
                        f"{event_id}"
                    ),
                ),
            ]
        )

    total_pages = (
        (len(events) + per_page - 1)
        // per_page
    )

    navigation = []

    if page > 0:
        navigation.append(
            button(
                "◀️ Previous",
                (
                    f"events_page_"
                    f"{category}_"
                    f"{page - 1}"
                ),
            )
        )

    if page < total_pages - 1:
        navigation.append(
            button(
                "Next ▶️",
                (
                    f"events_page_"
                    f"{category}_"
                    f"{page + 1}"
                ),
            )
        )

    if navigation:
        buttons.append(navigation)

    buttons.append(
        [
            button(
                "📂 Categories",
                "events",
                "success",
            ),
        ]
    )

    buttons.append(
        [
            button(
                "↩️ Back",
                "main_menu",
            ),
        ]
    )

    return {
        "inline_keyboard": buttons
    }


def event_detail_keyboard(
    category,
    page,
    event,
):
    buttons = []

    external_link = event.get(
        "external_link"
    )

    voice_link = event.get(
        "voice_link"
    )

    if external_link:
        buttons.append(
            [
                button(
                    "🔗 Event Link",
                    url=external_link,
                    style="success",
                ),
            ]
        )

    if voice_link:
        buttons.append(
            [
                button(
                    "🎙 Voice / Discord",
                    url=voice_link,
                ),
            ]
        )

    buttons.append(
        [
            button(
                "↩️ Event List",
                (
                    f"events_page_"
                    f"{category}_"
                    f"{page}"
                ),
                "success",
            ),
        ]
    )

    buttons.append(
        [
            button(
                "📂 Categories",
                "events",
            ),
        ]
    )

    buttons.append(
        [
            button(
                "↩️ Back",
                "main_menu",
            ),
        ]
    )

    return {
        "inline_keyboard": buttons
    }
