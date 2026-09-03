import html
from datetime import datetime, timedelta, timezone


GAME_TIME_EPOCH = datetime(
    2015,
    10,
    25,
    15,
    48,
    32,
    tzinfo=timezone(timedelta(hours=1)),
)


def updated_text():
    now = datetime.now(timezone.utc)

    return now.strftime(
        "🕐 Updated: %Y-%m-%d %H:%M UTC"
    )


def welcome_message():
    return (
        "🚛 <b>TruckersMP Status</b>\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "Welcome! 👋\n\n"
        "I'm your TruckersMP information bot.\n\n"
        "Check live server status, player counts, "
        "game time and other TruckersMP information.\n\n"
        "Choose an option below:"
    )


def _on_off(value):
    return "On" if value else "Off"


def _format_server(server):
    online = server.get("online", False)

    status = "🟢" if online else "🔴"

    name = html.escape(
        str(server.get("name", "Unknown"))
    )

    players = server.get("players", 0)
    max_players = server.get("maxplayers", 0)

    queue = server.get("queue", 0)

    collisions = server.get(
        "collisions",
        False,
    )

    speed_limiter = server.get(
        "speedlimiter",
        False,
    )

    promods = server.get(
        "promods",
        False,
    )

    afk_enabled = server.get(
        "afkenabled",
        False,
    )

    text = (
        f"{status} <b>{name}</b>\n"
        f"👥 <b>{players:,}</b> / {max_players:,}\n"
        f"💥 Collisions: "
        f"<b>{_on_off(collisions)}</b>\n"
        f"🚦 Speed Limiter: "
        f"<b>{_on_off(speed_limiter)}</b>"
    )

    if queue > 0:
        text += (
            f"\n⏳ Queue: <b>{queue:,}</b>"
        )

    if promods:
        text += (
            "\n🗺️ <b>ProMods Required</b>"
        )

    if afk_enabled:
        text += "\n💤 AFK Enabled"

    return text


def format_servers(servers):
    if servers is None:
        return (
            "⚠️ <b>TruckersMP API unavailable</b>\n\n"
            "Please try again later."
        )

    ets2_servers = []
    ats_servers = []
    event_servers = []
    special_servers = []

    for server in servers:
        if server.get("event"):
            event_servers.append(server)

        elif server.get("specialEvent"):
            special_servers.append(server)

        elif server.get("game") == "ETS2":
            ets2_servers.append(server)

        elif server.get("game") == "ATS":
            ats_servers.append(server)

    def sort_servers(items):
        items.sort(
            key=lambda server: server.get(
                "displayorder",
                9999,
            )
        )

    sort_servers(ets2_servers)
    sort_servers(ats_servers)
    sort_servers(event_servers)
    sort_servers(special_servers)

    text = (
        "🖥 <b>TruckersMP Servers</b>\n"
        "━━━━━━━━━━━━━━━━"
    )

    if ets2_servers:
        text += (
            "\n\n🚛 <b>Euro Truck Simulator 2</b>\n"
            "━━━━━━━━━━━━━━━━\n\n"
        )

        text += "\n\n".join(
            _format_server(server)
            for server in ets2_servers
        )

    if ats_servers:
        text += (
            "\n\n━━━━━━━━━━━━━━━━\n"
            "🇺🇸 <b>American Truck Simulator</b>\n"
            "━━━━━━━━━━━━━━━━\n\n"
        )

        text += "\n\n".join(
            _format_server(server)
            for server in ats_servers
        )

    if event_servers:
        text += (
            "\n\n━━━━━━━━━━━━━━━━\n"
            "🎉 <b>Event Servers</b>\n"
            "━━━━━━━━━━━━━━━━\n\n"
        )

        text += "\n\n".join(
            _format_server(server)
            for server in event_servers
        )

    if special_servers:
        text += (
            "\n\n━━━━━━━━━━━━━━━━\n"
            "⭐ <b>Special Event Servers</b>\n"
            "━━━━━━━━━━━━━━━━\n\n"
        )

        text += "\n\n".join(
            _format_server(server)
            for server in special_servers
        )

    text += (
        "\n\n━━━━━━━━━━━━━━━━\n"
        f"{updated_text()}"
    )

    return text


def format_status(servers):
    if servers is None:
        return (
            "⚠️ <b>TruckersMP API unavailable</b>\n\n"
            "Please try again later."
        )

    online = [
        server
        for server in servers
        if server.get("online")
    ]

    players = sum(
        server.get("players", 0)
        for server in servers
    )

    return (
        "📊 <b>TruckersMP Status</b>\n"
        "━━━━━━━━━━━━━━━━\n\n"
        f"🟢 Online servers: <b>{len(online)}</b>\n"
        f"👥 Total players: <b>{players:,}</b>\n\n"
        f"{updated_text()}"
    )


def format_game_time(game_time):
    if game_time is None:
        return (
            "⚠️ <b>TruckersMP Game Time</b>\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "TruckersMP API unavailable."
        )

    game_datetime = (
        GAME_TIME_EPOCH
        + timedelta(minutes=game_time)
    )

    time_text = game_datetime.strftime(
        "%H:%M"
    )

    weekday = game_datetime.strftime(
        "%A"
    )

    return (
        "🕐 <b>TruckersMP Game Time</b>\n"
        "━━━━━━━━━━━━━━━━\n\n"
        f"⏱️ <b>Time on servers:</b> "
        f"{time_text}, {weekday}\n\n"
        "ℹ️ Game time is expressed in minutes, "
        "where 10 real seconds is 1 minute of "
        "in-game time. It is the number of minutes "
        "since 2015-10-25 15:48:32 CET.\n\n"
        f"{updated_text()}"
    )


def format_version(version):
    if version is None:
        return (
            "⚠️ <b>TruckersMP Version</b>\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "TruckersMP API unavailable.\n\n"
            "Please try again later."
        )

    name = html.escape(
        str(version.get("name", "Unknown"))
    )

    stage = html.escape(
        str(version.get("stage", "Unknown"))
    )

    ets2_version = html.escape(
        str(
            version.get(
                "supported_game_version",
                "Unknown",
            )
        )
    )

    ats_version = html.escape(
        str(
            version.get(
                "supported_ats_game_version",
                "Unknown",
            )
        )
    )

    release_time = html.escape(
        str(version.get("time", "Unknown"))
    )

    return (
        "🎮 <b>TruckersMP Versions</b>\n"
        "━━━━━━━━━━━━━━━━\n\n"

        "🚛 <b>TruckersMP Client</b>\n"
        f"📦 Version: <b>{name}</b>\n"
        f"🧪 Stage: <b>{stage}</b>\n\n"

        "━━━━━━━━━━━━━━━━\n\n"

        "🚛 <b>Euro Truck Simulator 2</b>\n"
        f"🎮 Supported Version: "
        f"<b>{ets2_version}</b>\n\n"

        "🇺🇸 <b>American Truck Simulator</b>\n"
        f"🎮 Supported Version: "
        f"<b>{ats_version}</b>\n\n"

        "━━━━━━━━━━━━━━━━\n"
        f"📅 Client Updated: "
        f"<b>{release_time} UTC</b>\n\n"
        f"{updated_text()}"
    )
