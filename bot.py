import os
import re
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
    print(f"ข้อความ: {message.content}", flush=True)
    
    # ไม่ตรวจข้อความของ Bot
    if message.author.bot:
        return

    # ตรวจหาลิงก์
    if re.search(r"https?://\S+|www\.\S+", message.content, re.IGNORECASE):
        try:
            await message.delete()
            print(f"ลบลิงก์จาก {message.author}: {message.content}", flush=True)

            warning = await message.channel.send(
                f"⚠️ {message.author.mention} ห้ามส่งลิงก์ในห้องนี้"
            )

            # ลบข้อความเตือนหลัง 5 วินาที
            await warning.delete(delay=5)

        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}", flush=True)



keep_alive()
bot.run(TOKEN)
