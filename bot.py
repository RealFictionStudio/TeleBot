from os import getenv
from discord import Intents, Interaction, Message, app_commands
from discord.ext import commands
from dotenv import load_dotenv

ALLOWED_TO_USE_SYNC = []
GROUPS = ["T1", "T2", "T3"]
SUBJECTS = ["ANL2", "PRM2", "SYCY"]
GUILDS = []

if not load_dotenv():
    print("No new Env Variables")

TOKEN = getenv("DISCORD_TOKEN")
if TOKEN == None:
    exit(-1)


def is_owner(ctx: commands.Context[commands.Bot]):
    return ctx.author.id in ALLOWED_TO_USE_SYNC


intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Player that is ready: {bot.user}")


@bot.listen("on_message")
async def on_message(message: Message):
    print(f"Message from {message.author} : {message.content}")
    if message.author != bot.user and "blob" in message.content:
        _ = await message.channel.send("blob")


@bot.command(name="sync", description="Owners Only, sync commands")
@commands.check(is_owner)
async def sync(ctx: commands.Context[commands.Bot]):
    print(f"Sync commands {bot.tree.get_commands().__len__()}")

    if ctx.guild == None:
        print("Couldn't get guild to sync with")
        return

    cmdsynced = await bot.tree.sync(guild=ctx.guild)

    _ = await ctx.send(f"Commands Synced: {len(cmdsynced)}")


@bot.tree.command()
@app_commands.guilds(*GUILDS)
@app_commands.describe(
    date="A date in format of dd(sep)mm(sep)yy where (sep) = - or / or :"
)
@app_commands.choices(
    group=[app_commands.Choice(name=group, value=group) for group in GROUPS],
    subject=[app_commands.Choice(name=subject, value=subject) for subject in SUBJECTS],
)
async def add_event(
    interaction: Interaction, date: str, group: str, subject: str, event: str
):
    """Adds described event to calendar using sqlite db"""
    print("Adding event: ")
    _ = await interaction.response.send_message(
        f"There will be {event} for {group} in {subject} at {date}"
    )


bot.run(TOKEN)
