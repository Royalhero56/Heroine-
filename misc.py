# modules/misc.py
from pyrogram import filters


def register(app, helpers):
    # placeholder for future features: media downloader, inline handlers etc.
    @app.on_message(filters.command("info"))
    async def info_cmd(client, message):
        await message.reply_text("HEROIN-style bot modular skeleton. Add modules in /modules folder.")
