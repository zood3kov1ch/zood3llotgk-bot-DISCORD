import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# --- Фейковый веб-сервер для Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --------------------------------------

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Твои ID каналов
WELCOME_CHANNEL_ID       = 1555672103280447589
RULES_CHANNEL_ID         = 1555657921638174731
ANNOUNCEMENTS_CHANNEL_ID = 1555896769156481084

# Токен берем из переменных окружения (для безопасности) или вставь свой
BOT_TOKEN = os.getenv("BOT_TOKEN")

@bot.event
async def on_ready():
    print(f"Бот успешно запущен в облаке: {bot.user}")
    await bot.change_presence(activity=discord.Game(name="PrismaticaX | 24/7"))

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    count = member.guild.member_count
    if 11 <= (count % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(count % 10, "th")

    embed = discord.Embed(
        description=(
            f"**Where to go next:**\n"
            f"• **Rules:** Make sure to check <#{RULES_CHANNEL_ID}>\n"
            f"• **Announcements:** Stay tuned in <#{ANNOUNCEMENTS_CHANNEL_ID}>\n\n"
            f"Make sure to read the rules and enjoy your stay!"
        ),
        color=0x2b2d31
    )

    if member.guild.icon:
        embed.set_thumbnail(url=member.guild.icon.url)

    embed.set_footer(text=f"{member.guild.name} • {count}{suffix} Member")

    await channel.send(f"Welcome {member.mention} to **{member.guild.name}**!", embed=embed)

# Запускаем поддержку жизни и самого бота
keep_alive()
bot.run(BOT_TOKEN)