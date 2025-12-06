import os
from pyrogram import Client
import importlib

modules = [
    "modules.basic",
    "modules.admin",
    "modules.game",
    "modules.ai_chat",
    "modules.users"
]

app = Client(
    "heroin-bot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

for m in modules:
    importlib.import_module(m)

app.run()
