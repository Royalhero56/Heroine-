# modules/basic.py
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def register(app, helpers):
    save_user = helpers.get("save_user")

    @app.on_message(filters.private & filters.command("start"))
    async def start_cmd(client, message):
        # save user to DB
        await save_user(message.from_user)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Help", callback_data="help_cb")]])
        await message.reply_text(
            "Hello! This is your modular HEROIN-style bot.\nUse /help to see commands.",
            reply_markup=kb,
        )

    @app.on_callback_query(filters.regex(r"^help_cb$"))
    async def cb_help(client, cq):
        await cq.answer()
        await cq.message.edit_text("Available commands:\n/start\n/help\n/ping\n/broadcast (owner)")

    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        await message.reply_text("Available commands:\n/start\n/help\n/ping\n/broadcast (owner)")

    @app.on_message(filters.command("ping"))
    async def ping_cmd(client, message):
        import time
        t1 = time.time()
        m = await message.reply_text("Pinging...")
        t2 = time.time()
        ms = int((t2 - t1) * 1000)
        await m.edit_text(f"Pong! `{ms} ms`")
