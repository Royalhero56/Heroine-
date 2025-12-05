# modules/echo.py
from pyrogram import filters


def register(app, helpers):
    save_user = helpers.get("save_user")

    @app.on_message(filters.private & filters.text & ~filters.command)
    async def echo(client, message):
        await save_user(message.from_user)
        await message.reply_text(f"Echo: {message.text}")
