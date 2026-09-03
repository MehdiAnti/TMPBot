import html
import re

from datetime import datetime


def format_events(events_data):
    if events_data is None:
        return (
            "⚠️ <b>TruckersMP Events</b>\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "TruckersMP API unavailable.\n\n"
            "Please try again later."
        )

    response = events_data.get(
        "response",
        {},
    )

    featured = response.get(
        "featured",
        [],
    )

    today = response.get(
        "today",
        [],
    )

    return (
        "📅 <b>TruckersMP Events</b>\n"
        "━━━━━━━━━━━━━━━━\n\n"
        f"⭐ Featured Events: "
        f"<b>{len(featured)}</b>\n"
        f"📆 Today's Events: "
        f"<b>{len(today)}</b>\n\n"
        "Choose a category below:"
    )


def format_event_time(value):
    if not value:
        return "Unknown"

    try:
        date = datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S",
        )

        return date.strftime(
            "%d %b %Y, %H:%M UTC",
        )

    except ValueError:
        return value


def clean_event_text(text):
    if not text:
        return ""

    text = re.sub(
        r"!\[.*?\]\(.*?\)",
        "",
        text,
    )

    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text,
    )

    text = re.sub(
        r"^#{1,6}\s*",
        "",
        text,
        flags=re.MULTILINE,
    )

    text = re.sub(
        r"^>\s?",
        "",
        text,
        flags=re.MULTILINE,
    )

    text = text.replace(
        "**",
        "",
    )

    text = re.sub(
        r"(?<!\*)\*([^*]+)\*(?!\*)",
        r"\1",
        text,
    )

    text = re.sub(
        r"^-{3,}\s*$",
        "━━━━━━━━━━━━━━━━",
        text,
        flags=re.MULTILINE,
    )

    text = html.escape(text)

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def format_event(
    event,
    event_index,
    total_events,
):
    name = html.escape(
        str(event.get(
            "name",
            "Unknown Event",
        ))
    )

    game = html.escape(
        str(event.get(
            "game",
            "Unknown",
        ))
    )

    event_type = html.escape(
        str(
            event.get(
                "event_type",
                {},
            ).get(
                "name",
                "Unknown",
            )
        )
    )

    server = html.escape(
        str(
            event.get(
                "server",
                {},
            ).get(
                "name",
                "Unknown",
            )
        )
    )

    language = html.escape(
        str(event.get(
            "language",
            "Unknown",
        ))
    )

    departure = event.get(
        "departure",
        {},
    )

    arrival = event.get(
        "arrive",
        {},
    )

    departure_city = html.escape(
        str(
            departure.get(
                "city",
                "Unknown",
            )
        )
    )

    departure_location = html.escape(
        str(
            departure.get(
                "location",
                "",
            )
        )
    )

    arrival_city = html.escape(
        str(
            arrival.get(
                "city",
                "Unknown",
            )
        )
    )

    arrival_location = html.escape(
        str(
            arrival.get(
                "location",
                "",
            )
        )
    )

    meetup_at = format_event_time(
        event.get("meetup_at")
    )

    start_at = format_event_time(
        event.get("start_at")
    )

    attendance = event.get(
        "attendances",
        {},
    )

    confirmed = attendance.get(
        "confirmed",
        0,
    )

    unsure = attendance.get(
        "unsure",
        0,
    )

    vtcs = attendance.get(
        "vtcs",
        0,
    )

    description = clean_event_text(
        event.get(
            "description",
            "",
        )
    )

    text = (
        f"📅 <b>{name}</b>\n"
        "━━━━━━━━━━━━━━━━\n\n"
        f"📌 Event "
        f"<b>{event_index + 1}/{total_events}</b>\n"
        f"🎮 Game: <b>{game}</b>\n"
        f"🚛 Type: <b>{event_type}</b>\n"
        f"🖥 Server: <b>{server}</b>\n"
        f"🌐 Language: <b>{language}</b>\n\n"

        "📍 <b>Route</b>\n"
        f"🚩 Departure: "
        f"<b>{departure_city}</b>"
    )

    if departure_location:
        text += (
            "\n📌 Location: "
            f"<b>{departure_location}</b>"
        )

    text += (
        f"\n🏁 Arrival: "
        f"<b>{arrival_city}</b>"
    )

    if arrival_location:
        text += (
            "\n📌 Location: "
            f"<b>{arrival_location}</b>"
        )

    text += (
        "\n\n🕐 <b>Schedule</b>\n"
        f"👋 Meetup: <b>{meetup_at}</b>\n"
        f"🚀 Start: <b>{start_at}</b>\n\n"

        "👥 <b>Attendance</b>\n"
        f"✅ Confirmed: <b>{confirmed}</b>\n"
        f"❓ Unsure: <b>{unsure}</b>\n"
        f"🏢 VTCs: <b>{vtcs}</b>"
    )

    if description:
        max_description = 1800

        if len(description) > max_description:
            description = (
                description[:max_description]
                + "..."
            )

        text += (
            "\n\n━━━━━━━━━━━━━━━━\n"
            "📝 <b>Description</b>\n\n"
            f"{description}"
        )

    return text
