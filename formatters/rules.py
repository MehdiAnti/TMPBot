def format_rules(data):
    if data is None:
        return (
            "⚠️ <b>TruckersMP Rules</b>\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "TruckersMP API unavailable.\n\n"
            "Please try again later."
        )

    revision = data.get(
        "revision",
        "Unknown",
    )

    return (
        "📜 <b>TruckersMP Rules</b>\n"
        "━━━━━━━━━━━━━━━━\n\n"

        f"📌 Revision: <b>{revision}</b>\n\n"

        "Select a category below to read the "
        "official TruckersMP rules.\n\n"

        "📚 <b>Available Sections</b>\n\n"

        "1️⃣ Service-wide Rules\n"
        "2️⃣ Game Only Rules\n"
        "3️⃣ Save Editing\n"
        "4️⃣ Forum Rules\n"
        "5️⃣ Disclaimer & Information\n\n"

        "━━━━━━━━━━━━━━━━\n"
        "ℹ️ Rules are loaded directly from "
        "the TruckersMP API."
    )
