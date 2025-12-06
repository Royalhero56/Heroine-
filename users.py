import os
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

mongo = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = mongo.users

@Client.on_message(filters.private)
async def save_user(client, message):
    await db.users.update_one(
        {"id": message.from_user.id},
        {"$set": {"name": message.from_user.first_name}},
        upsert=True
    )
