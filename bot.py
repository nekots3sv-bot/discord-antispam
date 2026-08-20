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

    if message.author.bot:
        return

    print(f"{message.author}: {message.content}")

    await bot.process_commands(message)


keep_alive()
bot.run(TOKEN)