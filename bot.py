import os
import asyncio
import logging
from importlib import import_module
from dotenv import load_dotenv
from pyrogram import Client

# ---------- Event loop fix for hosting (Python 3.14) ----------
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# --------------------------------------------------------------

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID") or 0)
API_HASH = os.getenv("API_HASH")
OWNER_ID = int(os.getenv("OWNER_ID") or 0)
MONGO_URL = os.getenv("MONGO_URL")

if not BOT_TOKEN or not API_ID or not API_HASH or not MONGO_URL:
    raise SystemExit("Please set BOT_TOKEN, API_ID, API_HASH and MONGO_URL environment variables.")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create Pyrogram client (bot)
app = Client("heroin-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Lazy import motor here to avoid import overhead when checking syntax
from motor.motor_asyncio import AsyncIOMotorClient
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["heroin_bot"]
users_collection = db["users"]

# Helper functions passed to modules
async def save_user(user):
    """Save user id (int) into users collection if not exists."""
    if not user:
        return
    uid = int(user.id if hasattr(user, "id") else user)
    existing = await users_collection.find_one({"user_id": uid})
    if not existing:
        await users_collection.insert_one({"user_id": uid})
        logger.info(f"Saved new user: {uid}")

helpers = {"save_user": save_user, "OWNER_ID": OWNER_ID, "db": db}

# Dynamically load modules from `modules` package
MODULES = [
    "modules.basic",
    "modules.admin",
    "modules.echo",
    "modules.misc",
]

for mod in MODULES:
    try:
        m = import_module(mod)
        if hasattr(m, "register"):
            m.register(app, helpers)
            logger.info(f"Registered module: {mod}")
        else:
            logger.warning(f"Module {mod} has no register(app, helpers) function")
    except Exception as e:
        logger.exception(f"Failed to import module {mod}: {e}")

if __name__ == "__main__":
    logger.info("Starting heroin-style bot...")
    app.run()
