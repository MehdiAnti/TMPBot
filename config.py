import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")

PORT = int(os.getenv("PORT", "10000"))


if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is missing"
    )


if not WEBHOOK_URL:
    raise RuntimeError(
        "RENDER_EXTERNAL_URL environment variable is missing"
    )
