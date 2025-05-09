import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Benutzername (ohne #1234) und Zielkanal
WATCH_USERNAME = "blobbbie"
TARGET_CHANNEL_ID = int("1362778383401877644")

# speichert wann der Benutzer deaf wurde
deaf_start_time = {}

@bot.event
async def on_ready():
    print(f"Bot eingeloggt als {bot.user}")
    check_deaf.start()

@bot.event
async def on_voice_state_update(member, before, after):
    if member.name != WATCH_USERNAME:
        return

    if not before.self_deaf and after.self_deaf:
        deaf_start_time[member.id] = datetime.utcnow()
    elif before.self_deaf and not after.self_deaf:
        deaf_start_time.pop(member.id, None)

@tasks.loop(seconds=5)
async def check_deaf():
    now = datetime.utcnow()
    for guild in bot.guilds:
        for member in guild.members:
            if member.name != WATCH_USERNAME:
                continue
            if member.id in deaf_start_time:
                if now - deaf_start_time[member.id] >= timedelta(seconds=3):
                    if member.voice:
                        target_channel = guild.get_channel(TARGET_CHANNEL_ID)
                        if target_channel:
                            await member.move_to(target_channel)
                            deaf_start_time.pop(member.id, None)

bot.run("MTM3MDQwMzkwNDkxNDcxODczMA.GFG_sB.eNmUZ6aRPOETXcxYYQR8WqTxvsCxBuarnpPlts")
