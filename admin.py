# modules/admin.py
from pyrogram import filters


def register(app, helpers):
    save_user = helpers.get("save_user")
    OWNER_ID = int(helpers.get("OWNER_ID") or 0)
    db = helpers.get("db")
    users_col = db["users"]

    @app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
    async def broadcast_cmd(client, message):
        # usage: /broadcast your message here
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("Usage: /broadcast Your message here")

        text = parts[1]
        sent = 0
        failed = 0
        async for u in users_col.find({}, {"user_id": 1}):
            try:
                await client.send_message(u["user_id"], text)
                sent += 1
            except Exception:
                failed += 1
        await message.reply_text(f"Broadcast finished. Sent: {sent}, Failed: {failed}")

    @app.on_message(filters.command("users") & filters.user(OWNER_ID))
    async def users_count(client, message):
        cnt = await users_col.count_documents({})
        await message.reply_text(f"Total users: {cnt}")
