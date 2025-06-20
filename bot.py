import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1361361112028942406
CHANNEL_ID = 1385273932449579008
BUYER_ROLE_ID = 1361369131756027906
THUMBNAIL_URL = "https://pbs.twimg.com/profile_images/1292988666709590016/JdM4lT5n_400x400.jpg"

participants = set()
embed_message = None
start_time = None
end_time = None
giveaway_finished = False

PARTICIPANTS_FILE = "participants.json"
GIVEAWAY_FILE = "giveaway_data.json"

def save_participants():
    with open(PARTICIPANTS_FILE, "w") as f:
        json.dump(list(participants), f)

def load_participants():
    global participants
    try:
        with open(PARTICIPANTS_FILE, "r") as f:
            participants.update(json.load(f))
    except FileNotFoundError:
        participants.clear()

def save_giveaway_time():
    with open(GIVEAWAY_FILE, "w") as f:
        json.dump({"start": start_time.isoformat()}, f)

def load_giveaway_time():
    global start_time, end_time
    try:
        with open(GIVEAWAY_FILE, "r") as f:
            data = json.load(f)
            start_time = datetime.fromisoformat(data["start"])
            end_time = start_time + timedelta(days=7)
    except FileNotFoundError:
        pass

def format_time_left(delta):
    if delta.total_seconds() <= 0:
        return "Finalizado"
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

class ParticipateButton(discord.ui.View):
    def __init__(self, disabled=False):
        super().__init__(timeout=None)
        self.disabled_state = disabled
        self.add_item(discord.ui.Button(
            label="🎁 Participar",
            style=discord.ButtonStyle.green,
            custom_id="participate_button",
            disabled=disabled
        ))

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    load_participants()
    load_giveaway_time()

    if start_time and end_time:
        await resume_giveaway()
    else:
        await start_new_giveaway()

async def start_new_giveaway():
    global start_time, end_time, embed_message
    channel = bot.get_channel(CHANNEL_ID)
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(days=7)
    save_giveaway_time()

    embed = generate_embed()
    embed_message = await channel.send(embed=embed, view=ParticipateButton())
    update_embed_loop.start()

async def resume_giveaway():
    global embed_message
    channel = bot.get_channel(CHANNEL_ID)
    async for msg in channel.history(limit=50):
        if msg.author == bot.user and msg.embeds:
            embed_message = msg
            break
    update_embed_loop.start()

def generate_embed():
    now = datetime.utcnow()
    time_left = end_time - now if end_time else timedelta(0)
    time_str = format_time_left(time_left)

    embed = discord.Embed(
        title="🎉 100 Twitch Primes",
        description=(
            f"**Participantes:** {len(participants)}\n"
            f"**Ganadores:** 4\n"
            f"**Premio:** 25 Twitch Primes por persona\n"
            f"**Finaliza en:** `{time_str}`"
        ),
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    return embed

@tasks.loop(seconds=10)
async def update_embed_loop():
    global giveaway_finished
    if not embed_message or giveaway_finished:
        return

    now = datetime.utcnow()
    if now >= end_time:
        giveaway_finished = True
        await finish_giveaway()
        return

    try:
        await embed_message.edit(embed=generate_embed(), view=ParticipateButton())
    except discord.NotFound:
        pass
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.data.get("custom_id") != "participate_button":
        return

    user = interaction.user
    guild = bot.get_guild(GUILD_ID)
    member = guild.get_member(user.id)

    if user.id in participants:
        await interaction.response.send_message("❌ Ya estás participando en el sorteo.", ephemeral=True)
        return

    if not any(role.id == BUYER_ROLE_ID for role in member.roles):
        await interaction.response.send_message("⚠️ Debes tener el rol de comprador para participar.", ephemeral=True)
        return

    participants.add(user.id)
    save_participants()
    await interaction.response.send_message("✅ ¡Estás participando en el sorteo!", ephemeral=True)

async def finish_giveaway():
    channel = bot.get_channel(CHANNEL_ID)

    if len(participants) < 4:
        await channel.send("⚠️ El sorteo ha finalizado, pero no hay suficientes participantes para seleccionar 4 ganadores.")
    else:
        winners = random.sample(list(participants), 4)
        mentions = [f"<@{uid}>" for uid in winners]
        embed = discord.Embed(
            title="🏆 ¡Sorteo Finalizado!",
            description=(
                "🎉 **Ganadores del sorteo de Twitch Primes:**\n\n" +
                "\n".join(mentions)
            ),
            color=discord.Color.gold()
        )
        embed.set_footer(text="¡Gracias a todos por participar!")
        await channel.send(embed=embed)
    if embed_message:
        final_embed = generate_embed()
        view = ParticipateButton(disabled=True)
        try:
            await embed_message.edit(embed=final_embed, view=view)
        except discord.NotFound:
            pass

bot.run("TU_TOKEN")
