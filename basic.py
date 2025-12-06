rom pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Hello! I am a Human-like AI Bot + Game Bot!")

@Client.on_message(filters.command("help"))
async def help(client, message):
    await message.reply("/start\n/game\n/score\n/leaderboard\nJust type anything to chat 🤖")
