# modules/game.py
import random
from pyrogram import filters

# In-memory active games (per user)
ACTIVE_GAMES = {}


def register(app, helpers):
    save_user = helpers.get("save_user")
    db = helpers.get("db")
    scores = db["game_scores"]

    # ✅ Start new game
    @app.on_message(filters.private & filters.command("game"))
    async def start_game(client, message):
        await save_user(message.from_user)
        number = random.randint(1, 10)
        ACTIVE_GAMES[message.from_user.id] = number
        await message.reply_text(
            "🎮 *Number Guessing Game Started!*\n\n"
            "I have selected a number between *1 and 10*.\n"
            "Send your guess as a normal number!",
            quote=True
        )

    # ✅ Guess handler
    @app.on_message(filters.private & filters.text & ~filters.command)
    async def guess_handler(client, message):
        uid = message.from_user.id

        if uid not in ACTIVE_GAMES:
            return  # ignore if no game running

        try:
            guess = int(message.text.strip())
        except ValueError:
            return await message.reply_text("❌ Please send a valid number.")

        real = ACTIVE_GAMES.get(uid)

        if guess == real:
            # win
            del ACTIVE_GAMES[uid]
            await message.reply_text("🎉 *Correct! You won the game!* ✅")

            # update score in MongoDB
            user = await scores.find_one({"user_id": uid})
            if user:
                await scores.update_one({"user_id": uid}, {"$inc": {"wins": 1}})
            else:
                await scores.insert_one({"user_id": uid, "wins": 1})
        else:
            await message.reply_text("❌ Wrong number! Try again...")

    # ✅ Show score
    @app.on_message(filters.private & filters.command("score"))
    async def score_cmd(client, message):
        user = await scores.find_one({"user_id": message.from_user.id})
        wins = user.get("wins", 0) if user else 0
        await message.reply_text(f"🏆 Your total wins: *{wins}*")

    # ✅ Global leaderboard (top 10)
    @app.on_message(filters.command("leaderboard"))
    async def leaderboard_cmd(client, message):
        text = "🏆 *Top Players* 🏆\n\n"
        i = 1
        async for user in scores.find().sort("wins", -1).limit(10):
            text += f"{i}. User `{user['user_id']}` → {user.get('wins', 0)} wins\n"
            i += 1

        if i == 1:
            text += "No players yet!"

        await message.reply_text(text)
