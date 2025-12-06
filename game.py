import random
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
import os

mongo = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = mongo.game
users = {}

@Client.on_message(filters.command("game"))
async def start_game(client, message):
    num = random.randint(1, 10)
    users[message.from_user.id] = num
    await message.reply("🎮 Guess number between 1 to 10")

@Client.on_message(filters.text & filters.private)
async def guess_number(client, message):
    uid = message.from_user.id
    if uid not in users:
        return

    if message.text.isdigit():
        if int(message.text) == users[uid]:
            await message.reply("✅ Correct! You won the game!")
            await db.scores.update_one({"user": uid}, {"$inc": {"wins": 1}}, upsert=True)
        else:
            await message.reply("❌ Wrong! Try again.")

@Client.on_message(filters.command("score"))
async def score(client, message):
    data = await db.scores.find_one({"user": message.from_user.id})
    await message.reply(f"🏆 Your Score: {data['wins'] if data else 0}")
