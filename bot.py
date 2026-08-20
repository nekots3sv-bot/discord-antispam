import os
import discord
from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")


@bot.event
async def on_message(message):
    print("ON_MESSAGE ทำงานแล้ว", flush=True)
    if message.author.bot:
        return

    print(f"{message.author}: {message.content}")


keep_alive()
bot.run(TOKEN)
