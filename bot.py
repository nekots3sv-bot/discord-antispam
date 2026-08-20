import os
import re
import time
import discord
from keep_alive import keep_alive
from datetime import timedelta

# เก็บประวัติการส่ง Invite ของแต่ละคน
invite_warnings = {}

# ตั้งค่า
TIMEOUT_AFTER = 3       # ส่งครบ 3 ครั้ง -> Timeout
BAN_AFTER = 6           # ส่งครบ 6 ครั้ง -> Ban
TIME_WINDOW = 300       # นับเฉพาะภายใน 5 นาที
TIMEOUT_SECONDS = 600   # Timeout 10 นาที

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

    # ไม่ตรวจ Bot
    if message.author.bot:
        return

    # ตรวจ Discord Invite
    invite_pattern = r"(discord\.gg/|discord\.com/invite/)\S+"

    if re.search(invite_pattern, message.content, re.IGNORECASE):

        user_id = message.author.id
        now = time.time()

        try:
            # ลบข้อความ
            await message.delete()

            print(
                f"🗑️ ลบ Discord Invite จาก {message.author}: {message.content}",
                flush=True
            )

            # สร้างประวัติถ้ายังไม่มี
            if user_id not in invite_warnings:
                invite_warnings[user_id] = []

            # ลบประวัติเก่าที่เกิน 5 นาที
            invite_warnings[user_id] = [
                timestamp
                for timestamp in invite_warnings[user_id]
                if now - timestamp < TIME_WINDOW
            ]

            # เพิ่มครั้งนี้
            invite_warnings[user_id].append(now)

            count = len(invite_warnings[user_id])

            print(
                f"⚠️ {message.author} ส่ง Invite ครั้งที่ {count}",
                flush=True
            )

            # =========================
            # BAN
            # =========================
            if count >= BAN_AFTER:

                await message.guild.ban(
                    message.author,
                    reason="Discord Invite Spam"
                )

                print(
                    f"🚫 BAN: {message.author}",
                    flush=True
                )

                return

            # =========================
            # TIMEOUT
            # =========================
            if count >= TIMEOUT_AFTER:

                timeout_until = discord.utils.utcnow() + timedelta(
                    seconds=TIMEOUT_SECONDS
                )

                await message.author.timeout(
                    timeout_until,
                    reason="Repeated Discord Invite Spam"
                )

                warning = await message.channel.send(
                    f"🔇 {message.author.mention} ถูก Timeout 10 นาที "
                    f"เนื่องจากส่ง Discord Invite ซ้ำหลายครั้ง"
                )

                await warning.delete(delay=8)

                print(
                    f"🔇 TIMEOUT: {message.author}",
                    flush=True
                )

                return

            # =========================
            # WARNING
            # =========================

            warning = await message.channel.send(
                f"⚠️ {message.author.mention} กรุณาอย่าส่ง Discord Invite ในเซิร์ฟเวอร์นี้\n"
                f"การส่งซ้ำหลายครั้งอาจทำให้ถูก Timeout หรือ Ban"
            )

            await warning.delete(delay=8)

        except Exception as e:
            print(
                f"❌ เกิดข้อผิดพลาด: {e}",
                flush=True
            )



keep_alive()
bot.run(TOKEN)
