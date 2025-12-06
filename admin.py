import os
from pyrogram import Client, filters

OWNER = int(os.getenv("OWNER_ID"))

@Client.on_message(filters.command("broadcast") & filters.user(OWNER))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to message to broadcast")

    users = await client.get_dialogs()
    for u in users:
        try:
            await message.reply_to_message.copy(u.chat.id)
        except:
            pass
