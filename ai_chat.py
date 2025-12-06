import os
from pyrogram import Client, filters
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

@Client.on_message(filters.text & ~filters.command)
async def ai_chat(client, message):
    if not openai.api_key:
        return

    try:
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly human-like assistant."},
                {"role": "user", "content": message.text}
            ]
        )

        await message.reply_text(reply.choices[0].message.content)

    except Exception as e:
        print("AI Error:", e)
